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

import importlib
import inspect
import logging
import os
import pkgutil
import re
from functools import lru_cache
from typing import Optional

from .context import ParsingContext
from ..exceptions import EdifactParserException
from ..mods.module_constants import EdifactMessageType

logger = logging.getLogger(__name__)


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

    def __init__(self):
        """
        Initialize the factory by registering all parsing contexts.

        This constructor creates a dictionary mapping EDIFACT message types to their respective
        context instances.
        """
        self.__contexts: dict[EdifactMessageType, ParsingContext] = {}
        self.__register_contexts()

    def __register_contexts(self) -> None:
        """
        Initialize and register the contexts dictionary with instances of all parsing contexts.
        """
        # Initialize contexts for each message type by discovering them in the mods folder
        self.__contexts = self.__discover_contexts()

    @staticmethod
    def __discover_contexts() -> dict[EdifactMessageType, ParsingContext]:
        """
        Dynamically discover and instantiate all parsing contexts in the mods folder.

        Returns:
            A dictionary mapping message types to their respective parsing context instances.
        """
        contexts = {}

        # Get the path to the mods folder
        mods_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mods')

        # Iterate through all modules in the mods folder
        for _, mod_name, is_pkg in pkgutil.iter_modules([mods_path]):
            if is_pkg:
                # Check if this module has a context.py file
                context_filename = "context.py"
                context_path = os.path.join(mods_path, mod_name, context_filename)

                if os.path.exists(context_path):
                    try:
                        # Import the module
                        module_name = f"..mods.{mod_name}.context"
                        module = importlib.import_module(module_name, package=__package__)

                        # Find all classes in the module that inherit from ParsingContext
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if issubclass(obj, ParsingContext) and obj != ParsingContext:
                                # Extract the message type from the class name
                                # The class name should follow the pattern <MessageType>ParsingContext
                                expected_suffix = "ParsingContext"
                                if name.endswith(expected_suffix):
                                    message_type_name = name.replace(expected_suffix, '')

                                    # Check if this message type is defined in the EdifactMessageType enum
                                    try:
                                        # Convert to uppercase to match the enum values
                                        message_type = EdifactMessageType(message_type_name.upper())
                                        # Instantiate the context and add it to the dictionary
                                        contexts[message_type] = obj()
                                    except ValueError:
                                        logger.warning(
                                            f"Message type {message_type_name} not found in EdifactMessageType enum."
                                        )
                    except (ImportError, AttributeError) as e:
                        logger.warning(f"Error importing parsing context for module {mod_name}: {e}.")

        return contexts

    def create_context(self, message_type: EdifactMessageType) -> ParsingContext:
        """
        Create a ParsingContext instance based on the message type.

        Args:
            message_type: The type of EDIFACT message.

        Returns:
            A ParsingContext instance appropriate for the message type.

        Raises:
            EdifactParserException: If the message type is not supported.
        """
        context = self.__contexts.get(message_type)
        if context:
            return context
        else:
            raise EdifactParserException(f"Unsupported message type: {message_type}")

    def identify_and_create_context(self, edifact_text: str, parsing_context: ParsingContext) -> ParsingContext:
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
            if self._find_message_type(edifact_text, message_type.value, parsing_context):
                return self.create_context(message_type)

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
        # Import EdifactSyntaxHelper here to avoid circular imports
        from ..utils import EdifactSyntaxHelper

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
