# coding: utf-8

import importlib
import inspect
import logging
import os
import pkgutil
from typing import Optional, Type, TypeVar, Generic

from . import SegmentConverter
from ..mods.module_constants import EdifactMessageType
from ..utils.edifact_syntax_helper import EdifactSyntaxHelper
from ..wrappers.constants import SegmentType
from ..wrappers.context import ParsingContext

logger = logging.getLogger(__name__)

T = TypeVar('T')


class SegmentConverterFactory(Generic[T]):
    """
    Factory class for creating segment converters.

    This factory maintains a registry of segment converters and provides a method to 
    retrieve the appropriate __converter for a given segment type and message type. It centralizes
    the creation and management of segment converters, ensuring that each segment type 
    is processed by its specialized __converter.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the factory with a syntax parser and register all segment converters.

        This constructor creates a dictionary mapping segment types to their respective
        __converter instances, initializing each __converter with the provided syntax parser.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components,
                           which will be passed to each __converter.
        """
        self.__syntax_parser = syntax_parser
        self.__converters: dict[str, SegmentConverter] = {}
        self.__register_converters(syntax_parser)

    def __register_converters(self, syntax_parser: EdifactSyntaxHelper) -> None:
        """
        Initialize and register the converters dictionary with instances of all segment converters.
        Automatically discovers and registers converters for all segment types defined in SegmentType enum.
        """
        # Initialize converters dictionary
        self.__converters = {}

        # Dynamically import and register converters for all segment types
        for segment_type in SegmentType:
            try:
                # Import the base __converter class dynamically
                module_name = f".{segment_type.value.lower()}_segment_converter"
                module = importlib.import_module(module_name, package=__package__)

                # Find the base __converter class
                converter_class_name = f"{segment_type.value}SegmentConverter"
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if name == converter_class_name:
                        # Create an instance of the base converter
                        base_converter = obj(syntax_parser)

                        # Discover message-type-specific converters
                        message_specific_converters = self.__discover_segment_converters(
                            segment_type.value, syntax_parser, obj
                        )

                        # If message-specific converters were found, store both the base converter
                        # and the message-specific converters in a dictionary structure
                        if message_specific_converters:
                            converter_dict = {
                                'base': base_converter,
                                'message_specific': message_specific_converters
                            }
                            self.__converters[segment_type.value] = converter_dict
                        else:
                            # If no message-specific converters were found, just store the base converter
                            self.__converters[segment_type.value] = base_converter
                        break
            except (ImportError, AttributeError) as e:
                logger.debug(f"No __converter found for segment type '{segment_type.value}': {e}")
                # Continue with the next segment type if this one doesn't have a __converter

    def __discover_segment_converters(self, segment_type: str, syntax_parser: EdifactSyntaxHelper, segment_converter_base: Type) -> dict[str, SegmentConverter]:
        """
        Dynamically discover and instantiate all segment converters of a specific type in the mods folder.

        Args:
            segment_type: The type of segment __converter to discover (e.g., "COM", "DTM").
            syntax_parser: The syntax parser to use for parsing segment components.
            segment_converter_base: The base class for the segment converters.

        Returns:
            A dictionary mapping message types to their respective segment __converter instances.
        """
        converters = {}

        # Get the path to the mods folder
        mods_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mods')

        # Iterate through all modules in the mods folder
        for _, mod_name, is_pkg in pkgutil.iter_modules([mods_path]):
            if is_pkg:
                # Check if this module has a converters/{segment_type}_segment_converter.py file
                converter_filename = f"{segment_type.lower()}_segment_converter.py"
                converter_path = os.path.join(mods_path, mod_name, 'converters', converter_filename)
                if os.path.exists(converter_path):
                    try:
                        # Import the module
                        module_name = f"..mods.{mod_name}.converters.{segment_type.lower()}_segment_converter"
                        module = importlib.import_module(module_name, package=__package__)

                        # Find all classes in the module that inherit from the segment __converter base class
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if issubclass(obj, segment_converter_base) and obj != segment_converter_base:
                                # Extract the message type from the class name
                                # The class name should follow the pattern <MessageType><SegmentType>SegmentConverter
                                expected_suffix = f"{segment_type}SegmentConverter"
                                if name.endswith(expected_suffix):
                                    message_type_name = name.replace(expected_suffix, '')

                                    # Check if this message type is defined in the EdifactMessageType enum
                                    try:
                                        message_type = EdifactMessageType(message_type_name)
                                        # Instantiate the __converter and add it to the dictionary
                                        converters[message_type] = obj(syntax_parser)
                                    except ValueError:
                                        logger.warning(
                                            f"Message type {message_type_name} not found in EdifactMessageType enum."
                                        )
                    except (ImportError, AttributeError) as e:
                        logger.warning(f"Error importing {segment_type} segment __converter for module {mod_name}: {e}.")

        return converters

    def get_converter(self, segment_type: str, context: Optional[ParsingContext] = None) -> Optional[SegmentConverter[T]]:
        """
        Get the __converter for the specified segment type.

        Args:
            segment_type: The segment type to get a __converter for.
            context: The parsing context, which contains information about the message type.
                    If provided, the __converter for the specific message type will be returned.
                    If no specific __converter is found, falls back to the base __converter.

        Returns:
            The __converter for the segment type, or None if no __converter is found.
        """
        converter_or_dict = self.__converters.get(segment_type)
        if not converter_or_dict:
            logger.warning(f"No __converter found for segment type '{segment_type}'.")
            return None

        # Check if the __converter is a dictionary with our new structure
        if isinstance(converter_or_dict, dict) and 'base' in converter_or_dict and 'message_specific' in converter_or_dict:
            # If we have a context with a message type, try to get the message-specific converter
            if context and context.message_type:
                message_specific_converters = converter_or_dict['message_specific']
                converter = message_specific_converters.get(context.message_type)
                if converter:
                    return converter

                # If no message-specific converter was found, fall back to the base converter
                logger.debug(
                    f"No __converter defined for segment type '{segment_type}' "
                    f"and message type '{context.message_type}'. "
                    f"Falling back to base __converter."
                )
                return converter_or_dict['base']
            else:
                # If no context or message type is provided, use the base converter
                logger.debug(f"No context or message type provided for segment type '{segment_type}'. Using base converter.")
                return converter_or_dict['base']
        # Check if the __converter is a dictionary of message-type-specific converters (old format)
        elif isinstance(converter_or_dict, dict):
            # If we have a context with a message type, use it to get the appropriate __converter
            if context and context.message_type:
                converter = converter_or_dict.get(context.message_type)
                if converter:
                    return converter

                logger.debug(
                    f"No __converter defined for segment type '{segment_type}' "
                    f"and message type '{context.message_type}'. "
                    f"Falling back to base __converter."
                )

                # Import the base __converter class dynamically
                try:
                    module_name = f".{segment_type.lower()}_segment_converter"
                    module = importlib.import_module(module_name, package=__package__)

                    # Find the base __converter class
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if name == f"{segment_type}SegmentConverter":
                            # Create an instance of the base __converter using the stored syntax parser
                            return obj(self.__syntax_parser)
                except (ImportError, AttributeError) as e:
                    logger.warning(f"Error importing base __converter for segment type '{segment_type}': {e}.")
                    return None
            else:
                # If no context or message type is provided, we can't determine which __converter to use
                logger.debug(f"No context or message type provided for segment type '{segment_type}'.")
                return None
        else:
            # If the __converter is not a dictionary, use it directly
            return converter_or_dict
