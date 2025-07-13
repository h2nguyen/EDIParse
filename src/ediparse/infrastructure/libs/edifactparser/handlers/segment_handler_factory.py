# coding: utf-8

import importlib
import inspect
import logging
import os
import pkgutil
from typing import Optional, Type

from .segment_handler import SegmentHandler
from ..mods.module_constants import EdifactMessageType
from ..utils.edifact_syntax_helper import EdifactSyntaxHelper
from ..wrappers.constants import SegmentType
from ..wrappers.context import ParsingContext

logger = logging.getLogger(__name__)


class SegmentHandlerFactory:
    """
    Factory class for creating segment handlers.

    This factory maintains a registry of segment handlers and provides a method to 
    retrieve the appropriate handler for a given segment type. It centralizes the 
    creation and management of segment handlers, ensuring that each segment type 
    is processed by its specialized handler.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the factory with a syntax parser and register all segment handlers.

        This constructor creates a dictionary mapping segment types to their respective
        handler instances, initializing each handler with the provided syntax parser.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components,
                           which will be passed to each handler.
        """
        self.__handlers: dict[str, SegmentHandler] = {}
        self.__register_handlers(syntax_parser)

    def __register_handlers(self, syntax_parser: EdifactSyntaxHelper) -> None:
        """
        Initialize and register the handlers dictionary with instances of all segment handlers.
        Automatically discovers and registers handlers for all segment types defined in SegmentType enum.
        """
        # Initialize handlers dictionary
        self.__handlers = {}

        # Dynamically import and register handlers for all segment types
        for segment_type in SegmentType:
            try:
                # Import the base handler class dynamically
                module_name = f".{segment_type.value.lower()}_segment_handler"
                module = importlib.import_module(module_name, package=__package__)

                # Find the base handler class
                handler_class_name = f"{segment_type.value}SegmentHandler"
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if name == handler_class_name:
                        # Discover message-type-specific handlers
                        message_specific_handlers = self.__discover_segment_handlers(
                            segment_type.value, syntax_parser, obj
                        )

                        # Check if the class is abstract
                        is_abstract = inspect.isabstract(obj)

                        if message_specific_handlers:
                            if not is_abstract:
                                # Create an instance of the base handler if it's not abstract
                                base_handler = obj(syntax_parser)
                                # Store both the base handler and message-specific handlers
                                handler_dict = {
                                    'base': base_handler,
                                    'message_specific': message_specific_handlers
                                }
                                self.__handlers[segment_type.value] = handler_dict
                            else:
                                # If the base class is abstract, only store the message-specific handlers
                                self.__handlers[segment_type.value] = message_specific_handlers
                        elif not is_abstract:
                            # If no message-specific handlers were found and the class is not abstract,
                            # just store the base handler
                            base_handler = obj(syntax_parser)
                            self.__handlers[segment_type.value] = base_handler
                        # If the class is abstract and no message-specific handlers were found,
                        # we don't register anything for this segment type
                        break
            except (ImportError, AttributeError) as e:
                logger.debug(f"No handler found for segment type '{segment_type.value}': {e}")
                # Continue with the next segment type if this one doesn't have a handler

    def __discover_segment_handlers(self, segment_type: str, syntax_parser: EdifactSyntaxHelper, segment_handler_base: Type) -> dict[str, SegmentHandler]:
        """
        Dynamically discover and instantiate all segment handlers of a specific type in the mods folder.

        Args:
            segment_type: The type of segment handler to discover (e.g., "COM", "DTM").
            syntax_parser: The syntax parser to use for parsing segment components.
            segment_handler_base: The base class for the segment handlers.

        Returns:
            A dictionary mapping message types to their respective segment handler instances.
        """
        handlers = {}

        # Get the path to the mods folder
        mods_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mods')

        # Iterate through all modules in the mods folder
        for _, mod_name, is_pkg in pkgutil.iter_modules([mods_path]):
            if is_pkg:
                # Check if this module has a handlers/{segment_type}_segment_handler.py file
                handler_filename = f"{segment_type.lower()}_segment_handler.py"
                handler_path = os.path.join(mods_path, mod_name, 'handlers', handler_filename)
                if os.path.exists(handler_path):
                    try:
                        # Import the module
                        module_name = f"..mods.{mod_name}.handlers.{segment_type.lower()}_segment_handler"
                        module = importlib.import_module(module_name, package=__package__)

                        # Find all classes in the module that inherit from the segment handler base class
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if issubclass(obj, segment_handler_base) and obj != segment_handler_base:
                                # Extract the message type from the class name
                                # The class name should follow the pattern <MessageType><SegmentType>SegmentHandler
                                expected_suffix = f"{segment_type}SegmentHandler"
                                if name.endswith(expected_suffix):
                                    message_type_name = name.replace(expected_suffix, '')

                                    # Check if this message type is defined in the EdifactMessageType enum
                                    try:
                                        message_type = EdifactMessageType(message_type_name)
                                        # Instantiate the handler and add it to the dictionary
                                        handlers[message_type] = obj(syntax_parser)
                                    except ValueError:
                                        logger.warning(
                                            f"Message type {message_type_name} not found in EdifactMessageType enum."
                                        )
                    except (ImportError, AttributeError) as e:
                        logger.warning(f"Error importing {segment_type} segment handler for module {mod_name}: {e}.")

        return handlers

    def get_handler(self, segment_type: str, context: Optional[ParsingContext] = None) -> Optional[SegmentHandler]:
        """
        Get the handler for the specified segment type.

        Args:
            segment_type: The segment type to get a handler for.
            context: The parsing context, which contains information about the message type.
                    If provided, the handler's ability to handle the context will be checked.

        Returns:
            The handler for the segment type, or None if no handler is found or if the handler
            cannot handle the provided context.
        """
        handler_or_dict = self.__handlers.get(segment_type)
        if not handler_or_dict:
            logger.warning(f"No handler found for segment type '{segment_type}'.")
            return None

        # Check if the handler is a dictionary with our new structure
        if isinstance(handler_or_dict, dict) and 'base' in handler_or_dict and 'message_specific' in handler_or_dict:
            # If we have a context with a message type, try to get the message-specific handler
            if context and context.message_type:
                message_specific_handlers = handler_or_dict['message_specific']
                handler = message_specific_handlers.get(context.message_type)
                if handler:
                    return handler

                # If no message-specific handler was found, fall back to the base handler
                logger.debug(
                    f"No handler defined for segment type '{segment_type}' "
                    f"and message type '{context.message_type}'. "
                    f"Falling back to base handler."
                )
                return handler_or_dict['base']
            else:
                # If no context or message type is provided, use the base handler
                logger.debug(f"No context or message type provided for segment type '{segment_type}'. Using base handler.")
                return handler_or_dict['base']
        # Check if the handler is a dictionary of message-type-specific handlers (for abstract base classes)
        elif isinstance(handler_or_dict, dict) and context and context.message_type:
            # If we have a context with a message type, use it to get the appropriate handler
            handler = handler_or_dict.get(context.message_type)
            if not handler:
                logger.debug(
                    f"No handler defined for segment type '{segment_type}' "
                    f"and message type '{context.message_type}'."
                )
                return None
            return handler
        # Check if the handler is a dictionary of message-type-specific handlers (old format)
        elif isinstance(handler_or_dict, dict):
            # If we have a context with a message type, use it to get the appropriate handler
            if context and context.message_type:
                handler = handler_or_dict.get(context.message_type)
                if not handler:
                    logger.debug(
                        f"No handler defined for segment type '{segment_type}' "
                        f"and message type '{context.message_type}'."
                    )
                    return None
            else:
                # If no context or message type is provided, we can't determine which handler to use
                logger.debug(f"No context or message type provided for segment type '{segment_type}'.")
                return None
        else:
            # If the handler is not a dictionary, use it directly
            handler = handler_or_dict

        # Check if the handler can handle this context
        if context and context.message_type:
            if not handler.can_handle(context):
                logger.debug(
                    f"Handler for segment type '{segment_type}' cannot be processed "
                    f"with the context's message type '{context.message_type}'."
                )
                return None

        return handler
