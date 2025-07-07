# coding: utf-8

import logging
import importlib
import inspect
import os
import pkgutil
from typing import Optional, Type

from ..utils.edifact_syntax_helper import EdifactSyntaxHelper
from ..wrappers.constants import SegmentType, EdifactMessageType
from ..wrappers.context import ParsingContext

from .segment_handler import SegmentHandler
from .bgm_segment_handler import BGMSegmentHandler
from .cci_segment_handler import CCISegmentHandler
from .dtm_segment_handler import DTMSegmentHandler
from .lin_segment_handler import LINSegmentHandler
from .loc_segment_handler import LOCSegmentHandler
from .nad_segment_handler import NADSegmentHandler
from .pia_segment_handler import PIASegmentHandler
from .qty_segment_handler import QTYSegmentHandler
from .rff_segment_handler import RFFSegmentHandler
from .sts_segment_handler import STSSegmentHandler
from .una_segment_handler import UNASegmentHandler
from .unb_segment_handler import UNBSegmentHandler
from .unh_segment_handler import UNHSegmentHandler
from .uns_segment_handler import UNSSegmentHandler
from .unt_segment_handler import UNTSegmentHandler
from .unz_segment_handler import UNZSegmentHandler
from .erc_segment_handler import ERCSegmentHandler
from .ftx_segment_handler import FTXSegmentHandler

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
        """
        # Import segment handler base classes only when needed to avoid circular imports
        from .com_segment_handler import COMSegmentHandler
        from .cta_segment_handler import CTASegmentHandler

        # Initialize handlers for each segment type
        self.__handlers = {
            SegmentType.UNA: UNASegmentHandler(syntax_parser),
            SegmentType.UNB: UNBSegmentHandler(syntax_parser),
            SegmentType.UNH: UNHSegmentHandler(syntax_parser),
            SegmentType.BGM: BGMSegmentHandler(syntax_parser),
            SegmentType.DTM: DTMSegmentHandler(syntax_parser),
            SegmentType.RFF: RFFSegmentHandler(syntax_parser),
            SegmentType.NAD: NADSegmentHandler(syntax_parser),
            SegmentType.CTA: self.__discover_segment_handlers(SegmentType.CTA.value, syntax_parser, CTASegmentHandler),
            SegmentType.COM: self.__discover_segment_handlers(SegmentType.COM.value, syntax_parser, COMSegmentHandler),
            SegmentType.UNS: UNSSegmentHandler(syntax_parser),
            SegmentType.LOC: LOCSegmentHandler(syntax_parser),
            SegmentType.CCI: CCISegmentHandler(syntax_parser),
            SegmentType.LIN: LINSegmentHandler(syntax_parser),
            SegmentType.PIA: PIASegmentHandler(syntax_parser),
            SegmentType.QTY: QTYSegmentHandler(syntax_parser),
            SegmentType.STS: STSSegmentHandler(syntax_parser),
            SegmentType.UNT: UNTSegmentHandler(syntax_parser),
            SegmentType.UNZ: UNZSegmentHandler(syntax_parser),
            SegmentType.ERC: ERCSegmentHandler(syntax_parser),
            SegmentType.FTX: FTXSegmentHandler(syntax_parser),
        }

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
                                        logger.debug(
                                            f"Registered {segment_type} segment handler "
                                            f"for message type {message_type}."
                                        )
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

        # Check if the handler is a dictionary of message-type-specific handlers
        if isinstance(handler_or_dict, dict):
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
                logger.debug(f"No context or message type provided for segment type '{segment_type}' angegeben.")
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
