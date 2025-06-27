# coding: utf-8
"""
Port interface for parsing EDIFACT messages.

This module defines the MessageParserPort interface, which is a primary port
in the Ports and Adapters (Hexagonal) architecture. It represents the boundary
between the domain and the application layer for message parsing operations.

The port follows the Dependency Inversion Principle, allowing the domain to
define the interface that the application layer must implement, rather than
depending directly on application-specific implementations.
"""

from abc import ABC, abstractmethod
from typing import Any


class MessageParserPort(ABC):
    """
    Abstract port interface for parsing EDIFACT-specific messages.

    This port defines the interface for components that can parse EDIFACT-specific
    message content and convert it into a structured format.
    """

    @abstractmethod
    def execute(self, edifact_specific_message_content: str, max_lines_to_parse: int = -1) -> Any:
        """
        Parses an EDIFACT-specific message content into a structured format.

        Args:
            edifact_specific_message_content (str): The EDIFACT-specific message content to parse
            max_lines_to_parse (int): The maximum number of lines to parse, defaults to -1 which means no parsing limit

        Returns:
            Any: The parsed message in a structured format
        """
        pass
