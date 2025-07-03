# coding: utf-8
"""
Use case for parsing EDIFACT messages.

This module provides a use case implementation for parsing EDIFACT messages
according to the Clean Architecture pattern. It implements the MessageParserPort
interface from the domain layer and uses the EdifactParser from the infrastructure
layer to perform the actual parsing.

The use case acts as a boundary between the domain and infrastructure layers,
ensuring that the domain logic remains independent of the specific parsing
implementation details.
"""

from typing import Any

from ediparse.domain.ports.inbound import MessageParserPort
from ediparse.infrastructure.libs.edifactparser.parser import EdifactParser


class ParseMessageUseCase(MessageParserPort):
    """
    Use case implementation for parsing EDIFACT-specific messages.

    This class implements the MessageParserPort interface and uses the
    EdifactParser to perform the actual parsing of EDIFACT-specific messages.

    Attributes:
        __parser (EdifactParser): The parser used to parse EDIFACT-specific messages
    """

    def __init__(self, parser: EdifactParser = None) -> None:
        """
        Initializes a new instance of the ParseMessageUseCase class or
        creates a new EdifactParser instance to use for parsing.

        Args:
            parser (EdifactParser): The EDIFACT parser to use, defaults to None,
        """
        self.__parser = parser or EdifactParser()

    def execute(self, edifact_specific_message_content: str, max_lines_to_parse: int = -1) -> Any:
        """
        Parses an EDIFACT-specific message content into a structured format.

        Args:
            edifact_specific_message_content (str): The EDIFACT-specific message content to parse
            max_lines_to_parse (int): The maximum number of lines to parse, defaults to -1 which means no parsing limit

        Returns:
            Any: The parsed message in a structured format (EdifactInterchange)
        """
        return self.__parser.parse(
            edifact_text=edifact_specific_message_content,
            max_lines_to_parse=max_lines_to_parse
        )
