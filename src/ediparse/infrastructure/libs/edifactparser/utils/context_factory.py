# coding: utf-8
"""
Factory for creating ParsingContext instances.

This module provides a factory class for creating instances of ParsingContext subclasses
based on the EDIFACT message type. It implements the Factory Method pattern to dynamically
create the appropriate context object for different message types (MSCONS, APERAK, etc.),
allowing the parser to handle different message formats with type-specific logic.

The factory includes methods for both explicit creation based on a known message type
and automatic identification of the message type from the raw EDIFACT text.
"""

import re
from functools import lru_cache
from typing import Optional

from . import EdifactSyntaxHelper
from ..exceptions import EdifactParserException
from ..wrappers.context import ParsingContext
from ..mods.module_constants import EdifactMessageType
from ..mods.aperak.context import APERAKParsingContext
from ..mods.mscons.context import MSCONSParsingContext


class ParsingContextFactory:
    """
    Factory class for creating ParsingContext instances.

    This class implements the Factory Method pattern to create appropriate ParsingContext
    subclasses based on the EDIFACT message type. It centralizes the creation logic and
    provides a consistent interface for obtaining context objects, hiding the complexity
    of context instantiation from the client code.

    The factory plays a crucial role in the parsing process by:
    1. Creating the appropriate context for a specific message type (MSCONS, APERAK, etc.)
    2. Identifying the message type from raw EDIFACT text
    3. Ensuring that message-specific parsing rules are applied correctly

    This design allows the parser to be extended with support for new message types
    without modifying existing code, following the Open/Closed Principle.
    """

    @staticmethod
    def create_context(message_type: EdifactMessageType) -> ParsingContext:
        """
        Create a ParsingContext instance based on the message type.

        Args:
            message_type: The type of EDIFACT message.

        Returns:
            A ParsingContext instance appropriate for the message type.

        Raises:
            ValueError: If the message type is not supported.
        """
        if message_type == EdifactMessageType.MSCONS:
            return MSCONSParsingContext()
        elif message_type == EdifactMessageType.APERAK:
            return APERAKParsingContext()
        else:
            raise EdifactParserException(f"Unsupported message type: {message_type}")

    @staticmethod
    def identify_and_create_context(edifact_text: str, parsing_context: ParsingContext) -> ParsingContext:
        """
        Identify the message type from the EDIFACT text and create an appropriate context.

        This method analyzes the raw EDIFACT text to determine the message type
        (MSCONS, APERAK, etc.) and then creates the appropriate context object
        for that message type.

        Args:
            edifact_text: The EDIFACT message text to analyze.
            parsing_context: The current parsing context, used to determine delimiters.

        Returns:
            A ParsingContext instance appropriate for the identified message type.

        Raises:
            EdifactParserException: If no valid message type is found in the EDIFACT message.
        """
        for message_type in EdifactMessageType:
            if ParsingContextFactory._find_message_type(edifact_text, message_type.value, parsing_context):
                return ParsingContextFactory.create_context(message_type)

        raise EdifactParserException("No valid message type found in the EDIFACT message.")

    @staticmethod
    def _find_message_type(string_content: str, message_type_value: str, parsing_context: ParsingContext) -> bool:
        """
        Check if the message type value is present in the EDIFACT text.

        This method constructs a search pattern using the appropriate delimiters
        from the parsing context and then searches for the message type value
        in the EDIFACT text.

        Args:
            string_content: The EDIFACT text to search in.
            message_type_value: The message type value to search for (e.g., "MSCONS", "APERAK").
            parsing_context: The current parsing context, used to determine delimiters.

        Returns:
            True if the message type value is found in the text, False otherwise.
        """
        prefix: str = EdifactSyntaxHelper.get_element_separator(parsing_context)
        suffix: str = EdifactSyntaxHelper.get_component_separator(parsing_context)
        message_type_value_with_prefix_and_suffix = f"{prefix}{message_type_value}{suffix}"
        return ParsingContextFactory.__find_first_match_ci(string_content, message_type_value_with_prefix_and_suffix) is not None

    @staticmethod
    def __find_first_match_ci(string_content: str, message_type_value: str) -> Optional[int]:
        """
        Find the first case-insensitive match of message_type_value in string_content.

        This method performs a case-insensitive search for the message type value
        in the EDIFACT text. It uses a compiled and cached regular expression
        for efficiency when the same pattern is searched multiple times.

        Args:
            string_content: The EDIFACT text to search in.
            message_type_value: The message type value pattern to search for.

        Returns:
            The index of the first match (0-based), or None if not found.
        """

        @lru_cache(maxsize=16)
        def get_pattern(n: str) -> re.Pattern:
            return re.compile(re.escape(n), re.IGNORECASE)

        match = get_pattern(message_type_value).search(string_content)
        return match.start() if match else None
