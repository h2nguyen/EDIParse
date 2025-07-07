# coding: utf-8

import importlib
import inspect
import logging
import os
import pkgutil
from typing import Optional, Type, TypeVar, Generic

from . import SegmentConverter
from .bgm_segment_converter import BGMSegmentConverter
from .cci_segment_converter import CCISegmentConverter
from .com_segment_converter import COMSegmentConverter
from .cta_segment_converter import CTASegmentConverter
from .dtm_segment_converter import DTMSegmentConverter
from .nad_segment_converter import NADSegmentConverter
from .sts_segment_converter import STSSegmentConverter
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
    retrieve the appropriate converter for a given segment type and message type. It centralizes 
    the creation and management of segment converters, ensuring that each segment type 
    is processed by its specialized converter.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the factory with a syntax parser and register all segment converters.

        This constructor creates a dictionary mapping segment types to their respective
        converter instances, initializing each converter with the provided syntax parser.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components,
                           which will be passed to each converter.
        """
        self.__converters: dict[str, SegmentConverter] = {}
        self.__register_converters(syntax_parser)

    def __register_converters(self, syntax_parser: EdifactSyntaxHelper) -> None:
        """
        Initialize and register the converters dictionary with instances of all segment converters.
        """
        # Initialize converters for each segment type
        self.__converters = {
            SegmentType.BGM: BGMSegmentConverter(syntax_parser),
            SegmentType.DTM: self.__discover_segment_converters(SegmentType.DTM.value, syntax_parser, DTMSegmentConverter),
            SegmentType.NAD: self.__discover_segment_converters(SegmentType.NAD.value, syntax_parser, NADSegmentConverter),
            SegmentType.STS: self.__discover_segment_converters(SegmentType.STS.value, syntax_parser, STSSegmentConverter),
            SegmentType.CTA: CTASegmentConverter(syntax_parser),
            SegmentType.COM: COMSegmentConverter(syntax_parser),
            SegmentType.CCI: CCISegmentConverter(syntax_parser),
            # Add other segment types as needed
        }

    def __discover_segment_converters(self, segment_type: str, syntax_parser: EdifactSyntaxHelper, segment_converter_base: Type) -> dict[str, SegmentConverter]:
        """
        Dynamically discover and instantiate all segment converters of a specific type in the mods folder.

        Args:
            segment_type: The type of segment converter to discover (e.g., "COM", "DTM").
            syntax_parser: The syntax parser to use for parsing segment components.
            segment_converter_base: The base class for the segment converters.

        Returns:
            A dictionary mapping message types to their respective segment converter instances.
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

                        # Find all classes in the module that inherit from the segment converter base class
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
                                        # Instantiate the converter and add it to the dictionary
                                        converters[message_type] = obj(syntax_parser)
                                    except ValueError:
                                        logger.warning(
                                            f"Message type {message_type_name} not found in EdifactMessageType enum."
                                        )
                    except (ImportError, AttributeError) as e:
                        logger.warning(f"Error importing {segment_type} segment converter for module {mod_name}: {e}.")

        return converters

    def get_converter(self, segment_type: str, context: Optional[ParsingContext] = None) -> Optional[SegmentConverter[T]]:
        """
        Get the converter for the specified segment type.

        Args:
            segment_type: The segment type to get a converter for.
            context: The parsing context, which contains information about the message type.
                    If provided, the converter for the specific message type will be returned.

        Returns:
            The converter for the segment type, or None if no converter is found.
        """
        converter_or_dict = self.__converters.get(segment_type)
        if not converter_or_dict:
            logger.warning(f"No converter found for segment type '{segment_type}'.")
            return None

        # Check if the converter is a dictionary of message-type-specific converters
        if isinstance(converter_or_dict, dict):
            # If we have a context with a message type, use it to get the appropriate converter
            if context and context.message_type:
                converter = converter_or_dict.get(context.message_type)
                if not converter:
                    logger.debug(
                        f"No converter defined for segment type '{segment_type}' "
                        f"and message type '{context.message_type}'."
                    )
                    return None
            else:
                # If no context or message type is provided, we can't determine which converter to use
                logger.debug(f"No context or message type provided for segment type '{segment_type}'.")
                return None
        else:
            # If the converter is not a dictionary, use it directly
            converter = converter_or_dict

        return converter
