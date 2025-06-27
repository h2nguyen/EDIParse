# coding: utf-8
"""
Service for parsing EDIFACT messages.

This module provides a service that coordinates the parsing of EDIFACT messages
using the appropriate use case. It acts as a facade for the parsing functionality,
simplifying the interface for clients and delegating the actual parsing work to
the use case.

The service follows the Clean Architecture pattern, where services coordinate
the flow of data between the domain layer and the adapters.
"""

from typing import Any

from ediparse.application.usecases.parse_message_usecase import ParseMessageUseCase


class ParserService:
    """
    Service for parsing EDIFACT-specific messages.

    This service uses the ParseMessageUseCase to parse EDIFACT-specific messages.

    Attributes:
        __parse_message_usecase (ParseMessageUseCase): The use case for parsing EDIFACT-specific messages
    """

    def __init__(self, parse_message_usecase: ParseMessageUseCase = None) -> None:
        """
        Initializes a new instance of the ParserService class.

        Creates a new ParseMessageUseCase instance to use for parsing if one is not provided.

        Args:
            parse_message_usecase (ParseMessageUseCase): The use case to use for parsing, defaults to None
        """
        self.__parse_message_usecase = parse_message_usecase or ParseMessageUseCase()

    def parse_message(self, message_content: str, max_lines_to_parse: int = -1) -> Any:
        """
        Parses an EDIFACT-specific message content into a structured format.

        This method uses the ParseMessageUseCase to parse the message content.

        Args:
            message_content (str): The content of the EDIFACT-specific message to parse
            max_lines_to_parse (int): The maximum number of lines to parse, defaults to -1 which indicates no parsing limit

        Returns:
            Any: The parsed message in a structured format (EdifactInterchange)
        """
        return self.__parse_message_usecase.execute(
            edifact_specific_message_content=message_content,
            max_lines_to_parse=max_lines_to_parse
        )
