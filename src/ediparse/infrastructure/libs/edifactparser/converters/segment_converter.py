# coding: utf-8

import logging
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

from ..exceptions import CONTRLException
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import EdifactConstants, SegmentGroup

logger = logging.getLogger(__name__)

T = TypeVar('T')


class SegmentConverter(ABC, Generic[T]):
    """
    Abstract base class for all segment converters in the EDIFACT parser.

    This class defines the interface for converting EDI segment components into 
    typed domain model objects. It handles exception management and provides a 
    consistent conversion pattern for all segment types.

    The generic type parameter T represents the specific segment model type that 
    a concrete converter implementation will return.

    Attributes:
        None
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the converter with the syntax parser to use for parsing segment components.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        self._syntax_parser = syntax_parser

    def convert(
            self,
            line_number: int,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> T:
        """
        Converts segment components to a typed domain model object.

        This method wraps the internal conversion logic with exception handling.
        If an exception occurs during conversion, it's caught, logged, and wrapped
        in a CONTRLException with detailed error information.

        Args:
            line_number: The line number in the EDI file where this segment appears
            element_components: List of segment components extracted from the EDI file
            last_segment_type: The type of the previous segment (e.g., 'UNH', 'BGM')
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            A typed domain model object of type T

        Raises:
            CONTRLException: If any error occurs during the conversion process
        """
        try:
            return self._convert_internal(element_components, last_segment_type, current_segment_group, context)
        except Exception as ex:
            error_message = f"CONTRL -> L{line_number} -> {element_components} -> {ex}"
            logger.error(error_message)
            raise CONTRLException(message=error_message)

    @abstractmethod
    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> T:
        """
        Internal method to convert segment components to a typed domain model object.

        This abstract method must be implemented by all concrete converter classes.
        It contains the specific logic for converting a particular segment type.

        Args:
            element_components: List of segment components extracted from the EDIFACT file
            last_segment_type: The type of the previous segment (e.g., 'UNH', 'BGM')
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            A typed domain model object of type T
        """
        pass

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        """
        Helper method to get a human-readable identifier name based on qualifier code.

        This method can be overridden by subclasses to provide specific mappings
        from qualifier codes to human-readable names, often depending on the
        current segment group context.

        Args:
            qualifier_code: The qualifier code from the segment
            current_segment_group: The current segment group being processed
            context: The parsing context containing the message type and segment group context information

        Returns:
            A human-readable identifier name, or None if no mapping exists
        """
        pass

    @staticmethod
    def _convert_decimal(string_number: str, context: ParsingContext) -> float:
        """
        Converts a string representation of a number to a float using the appropriate decimal mark.

        This method determines the decimal mark from the UNA service string advice in the parsing context.
        If the decimal mark is not available, it falls back to using a dot as the default decimal mark.

        Args:
            string_number: The string representation of the number to convert
            context: The parsing context containing the UNA service string advice with decimal mark information

        Returns:
            The converted floating-point number

        Raises:
            AttributeError: If the UNA decimal mark is None or empty (caught internally)
        """
        try:
            decimal_mark = context.interchange.una_service_string_advice.decimal_mark
            if decimal_mark is None or decimal_mark == "":
                raise AttributeError(f"UNA decimal_mark is None or empty.")
        except AttributeError as ex:
            decimal_mark = EdifactConstants.DOT_DECIMAL
            logger.warning(
                f"Decimal mark not found in UNA service string advice."
                f" Using '{EdifactConstants.DOT_DECIMAL}' as default value."
                f" Original error: '{ex}'"
            )
        number = string_number.replace(decimal_mark, EdifactConstants.DOT_DECIMAL)
        return float(number)
