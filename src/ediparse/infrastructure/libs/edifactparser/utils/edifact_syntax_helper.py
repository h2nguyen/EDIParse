# coding: utf-8
"""
Utility for handling EDIFACT syntax and parsing operations.

This module provides a helper class for working with EDIFACT syntax, including
methods for handling delimiters, splitting segments, elements, and components,
and processing escape sequences according to the EDIFACT standard.

The EDIFACT standard defines specific characters for separating segments, elements,
and components in a message. These characters can be specified in a UNA segment
(Service String Advice) at the beginning of a message, or default values are used.
This module helps manage these characters and apply them correctly during parsing.
"""

import logging
import re
from typing import Optional

from ..wrappers.context import ParsingContext
from ..wrappers.constants import EdifactConstants, SegmentType
from ..exceptions import MSCONSParserException

logger = logging.getLogger(__name__)


class EdifactSyntaxHelper:
    """
    Helper for handling EDIFACT syntax and string operations.

    This class provides methods for parsing EDIFACT messages,
    including segment terminators, element separators, component separators, and
    release indicators (escape characters). It also includes methods for splitting
    strings according to EDIFACT syntax rules, respecting escape sequences.

    The default delimiters can be overridden by a UNA segment (Service String Advice)
    at the beginning of an EDIFACT message.

    Attributes:
        None. The helper is stateless and operates on the provided context.
    """

    def __init__(self):
        """Initialize the EdifactSyntaxHelper."""
        pass

    @staticmethod
    def __context_is_not_valid(context: ParsingContext = None) -> bool:
        """
        Checks if the parsing context is valid for EDIFACT operations.

        A valid context must have an interchange with UNA service string advice.

        Args:
            context: The parsing context to validate.

        Returns:
            True if the context is not valid, False otherwise.
        """
        return (context is None
                or context.interchange is None
                or context.interchange.una_service_string_advice is None)

    @staticmethod
    def get_cleaned_value(value: str, context: ParsingContext = None) -> str:
        """
        Removes all release characters (escape characters) from the input string.

        In EDIFACT, release characters are used to escape special characters like
        separators. This method removes these release characters to get the clean value.

        Args:
            value: The input string that may contain release characters.
            context: The parsing context to retrieve the release indicator, if any.

        Returns:
            The string with all release characters removed.
        """
        if not value:
            return value

        release_char = EdifactSyntaxHelper.get_release_indicator(context)

        if value.endswith(release_char):
            value = value[:-1]

        pattern = re.escape(release_char) + "(.)"
        return re.sub(pattern, r"\1", value)

    @staticmethod
    def get_component_separator(context: ParsingContext = None) -> str:
        """
        Gets the component separator character from the parsing context.

        If the context is not valid, returns the default component separator.

        Args:
            context: The parsing context containing separator information, if any.

        Returns:
            The component separator character to use for parsing.
        """
        if EdifactSyntaxHelper.__context_is_not_valid(context=context):
            return EdifactConstants.DEFAULT_COMPONENT_SEPARATOR
        return (context.interchange.una_service_string_advice.component_separator
                or EdifactConstants.DEFAULT_COMPONENT_SEPARATOR)

    @staticmethod
    def get_element_separator(context: ParsingContext = None) -> str:
        """
        Gets the element separator character from the parsing context.

        If the context is not valid, returns the default element separator.

        Args:
            context: The parsing context containing separator information, if any.

        Returns:
            The element separator character to use for parsing.
        """
        if EdifactSyntaxHelper.__context_is_not_valid(context=context):
            return EdifactConstants.DEFAULT_ELEMENT_SEPARATOR
        return (context.interchange.una_service_string_advice.element_separator
                or EdifactConstants.DEFAULT_ELEMENT_SEPARATOR)

    @staticmethod
    def get_decimal_mark(context: ParsingContext = None) -> str:
        """
        Gets the decimal mark character from the parsing context.

        If the context is not valid, returns the default decimal mark.

        Args:
            context: The parsing context containing decimal mark information, if any.

        Returns:
            The decimal mark character to use for parsing.
        """
        if EdifactSyntaxHelper.__context_is_not_valid(context=context):
            return EdifactConstants.DEFAULT_DECIMAL_MARK
        return (context.interchange.una_service_string_advice.decimal_mark
                or EdifactConstants.DEFAULT_DECIMAL_MARK)

    @staticmethod
    def get_release_indicator(context: ParsingContext = None) -> str:
        """
        Gets the release indicator (escape character) from the parsing context.

        If the context is not valid, returns the default release indicator.
        The release indicator is used to escape special characters in EDIFACT messages.

        Args:
            context: The parsing context containing release indicator information, if any.

        Returns:
            The release indicator character to use for parsing.
        """
        if EdifactSyntaxHelper.__context_is_not_valid(context=context):
            return EdifactConstants.DEFAULT_RELEASE_INDICATOR
        return (context.interchange.una_service_string_advice.release_character
                or EdifactConstants.DEFAULT_RELEASE_INDICATOR)

    @staticmethod
    def get_reserved_indicator(context: ParsingContext = None) -> str:
        """
        Gets the reserved indicator character from the parsing context.

        If the context is not valid, returns the default reserved indicator.
        The reserved indicator is a character reserved for future use in EDIFACT.

        Args:
            context: The parsing context containing reserved indicator information, if any.

        Returns:
            The reserved indicator character to use for parsing.
        """
        if EdifactSyntaxHelper.__context_is_not_valid(context=context):
            return EdifactConstants.DEFAULT_RESERVED_INDICATOR
        return (context.interchange.una_service_string_advice.reserved
                or EdifactConstants.DEFAULT_RESERVED_INDICATOR)

    @staticmethod
    def get_segment_terminator(context: ParsingContext = None) -> str:
        """
        Gets the segment terminator character from the parsing context.

        If the context is not valid, returns the default segment terminator.
        The segment terminator marks the end of a segment in EDIFACT messages.

        Args:
            context: The parsing context containing segment terminator information, if any.

        Returns:
            The segment terminator character to use for parsing.
        """
        if EdifactSyntaxHelper.__context_is_not_valid(context=context):
            return EdifactConstants.DEFAULT_SEGMENT_TERMINATOR
        return (context.interchange.una_service_string_advice.segment_terminator
                or EdifactConstants.DEFAULT_SEGMENT_TERMINATOR)

    @staticmethod
    def split_segments(string_content: str, context: ParsingContext = None) -> list[str]:
        """
        Splits a string into segments using the segment terminator,
        which is part of the parsing context.

        Args:
            string_content: The input string to split.
            context: The context containing splitting information, if any.

        Returns:
            A list of string segments.
        """
        return EdifactSyntaxHelper.__escape_split(
            string_content=string_content,
            escape_symbol=EdifactSyntaxHelper.get_release_indicator(context),
            delimiter=EdifactSyntaxHelper.get_segment_terminator(context),
            include_escape_symbol=True
        )

    @staticmethod
    def split_components(
            string_content: str,
            context: ParsingContext = None,
            include_escape_symbol: bool = True,
    ) -> list[str]:
        """
        Splits a string into components using the component separator,
        which is part of the parsing context.

        Args:
            string_content: The input string to split.
            context: The context containing splitting information, if any.
            include_escape_symbol: The flag specifying whether the escape symbol is still kept within string.

        Returns:
            A list of string components with escaped separators preserved.
        """
        return EdifactSyntaxHelper.__escape_split(
            string_content=string_content,
            escape_symbol=EdifactSyntaxHelper.get_release_indicator(context),
            delimiter=EdifactSyntaxHelper.get_component_separator(context),
            include_escape_symbol=include_escape_symbol
        )

    @staticmethod
    def split_elements(
            string_content: str,
            context: ParsingContext = None,
            include_escape_symbol: bool = True,
    ) -> list[str]:
        """
        Splits a string into elements using the element separator,
        which is part of the parsing context.

        Args:
            string_content: The input string to split.
            context: The context containing splitting information, if any.
            include_escape_symbol: The flag specifying whether the escape symbol is still kept within string.

        Returns:
            A list of string elements with escaped separators preserved.
        """
        return EdifactSyntaxHelper.__escape_split(
            string_content=string_content,
            escape_symbol=EdifactSyntaxHelper.get_release_indicator(context),
            delimiter=EdifactSyntaxHelper.get_element_separator(context),
            include_escape_symbol=include_escape_symbol
        )

    @staticmethod
    def remove_invalid_prefix_from_segment_data(
            string_content: str,
            segment_types: Optional[list[str]],
            context: ParsingContext,
    ) -> str:
        """
        Removes invalid prefixes from EDIFACT segment data.

        Sometimes EDIFACT messages contain invalid prefixes before the segment type
        which are not part of the actual EDIFACT message. This method removes any arbitrary prefix
        that appears before a valid segment type.

        The method works by:
        1. First checking if the string starts with any valid segment type (using the faster startswith method)
        2. If no segment type is found at the beginning, it searches for segment types anywhere in the string
        3. If a segment type is found, it removes everything before that segment type
        4. If no segment type is found, it returns the original string

        Examples:
            - "[${test(TEST_DATA)}]:UNB+..." becomes "UNB+..."
            - "SOME_PREFIX:UNH+..." becomes "UNH+..."
            - "UNB+..." remains "UNB+..." (no prefix to remove)
            - "INVALID_DATA_WITHOUT_SEGMENT_TYPE" remains unchanged

        Args:
            string_content: The input string that may contain an invalid prefix.
            segment_types: A list of valid segment types. Must not be None, or an exception will be raised.
            context: The parsing context to retrieve.

        Returns:
            The string with the invalid prefix is removed, if present.

        Raises:
            MSCONSParserException: If segment_types is None.
        """
        if segment_types is None or len(segment_types) == 0:
            raise MSCONSParserException("Segment types must not be None nor empty")

        if not string_content:
            return string_content

        for segment_type in segment_types:
            if string_content.startswith(segment_type):
                return string_content

        for segment_type in segment_types:
            index = string_content.find(segment_type)
            if index > 0:
                line_number = context.segment_count
                logger.debug(
                    f"L{line_number} -> Removing invalid prefix from segment data '{string_content[:index]}' from '{string_content}'")
                return string_content[index:]

        return string_content

    @staticmethod
    def find_and_get_una_segment(edifact_text: str) -> Optional[str]:
        """
        Checks for the UNA segment in the EDIFACT text.
        Searches for the first hit string that starts with "UNA" and ends with the single quote "'"
        and has the size of exactly 9 characters.

        Args:
            edifact_text (str): The EDIFACT text to parse

        Returns:
            Optional[str]: The UNA segment if found, None otherwise
        """
        # Search for a string that starts with "UNA", ends with "'", and has exactly 9 characters
        match = re.search(fr"{SegmentType.UNA}.{{5}}'", edifact_text)
        if match and len(match.group()) == 9:
            una_segment_string = match.group()

            # If UNA is not in the beginning, log a warning
            if match.start() > 0:
                logger.debug(f"Removing invalid prefix from UNA segment '{edifact_text[:match.start()]}'")

            return una_segment_string

        return None

    @staticmethod
    def __escape_split(
            string_content: str,
            escape_symbol: str,
            delimiter: str,
            include_escape_symbol: bool = True,
    ) -> list[str]:
        """
        Splits a string by the given delimiter while respecting escape sequences.

        Args:
            string_content: The input string to split.
            escape_symbol: The character used to escape the delimiter.
            delimiter: The character to split on.

        Returns:
            A list of string segments with escaped delimiters preserved.
        """
        parts = []
        current = ""
        string_position = 0

        while string_position < len(string_content):
            char = string_content[string_position]

            if char == escape_symbol and string_position + 1 < len(string_content):
                if include_escape_symbol:
                    # Escape character found, include both the escape character and the next character literally
                    current += escape_symbol + string_content[string_position + 1]
                else:
                    # Escape character found, include the next character literally
                    current += string_content[string_position + 1]
                string_position += 2
            elif char == delimiter:
                # Delimiter found (not escaped), split here
                parts.append(current)
                current = ""
                string_position += 1
            else:
                current += char
                string_position += 1

        parts.append(current)
        return parts
