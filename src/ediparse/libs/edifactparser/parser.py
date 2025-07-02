# coding: utf-8

import logging
from typing import Optional

from .exceptions import EdifactParserException
from .resolvers.group_state_resolver_factory import GroupStateResolverFactory
from .utils import EdifactSyntaxHelper, ParsingContextFactory
from .handlers import SegmentHandlerFactory
from .wrappers.context import ParsingContext, InitialParsingContext
from .wrappers.segments import EdifactInterchange
from .wrappers.constants import EdifactConstants, SegmentType

logger = logging.getLogger(__name__)


class EdifactParser:
    """
    Parser for EDIFACT-specific messages according to the defined domain model.

    This class is responsible for parsing EDIFACT (Electronic Data Interchange for 
    Administration, Commerce and Transport) messages. It handles the segmentation
    of EDIFACT text, processes each segment with appropriate handlers, and builds
    a structured representation of the interchange.

    The parser uses a context-based approach to maintain state during parsing and
    delegates specific segment handling to specialized handlers. It also uses resolvers
    to determine the segment group context during parsing.
    """

    def __init__(
            self,
            handler_factory: Optional[SegmentHandlerFactory] = None,
            resolver_factory: Optional[GroupStateResolverFactory] = None
    ) -> None:
        self.__context: Optional[ParsingContext] = InitialParsingContext()
        self.__syntax_parser = EdifactSyntaxHelper()
        self.__handler_factory = handler_factory or SegmentHandlerFactory(self.__syntax_parser)
        self.__resolver_factory = resolver_factory or GroupStateResolverFactory()

    def parse(self, edifact_text: str, max_lines_to_parse: int = -1) -> EdifactInterchange:
        """
        Main method: Reads the EDIFACT-specific message string, splits it at the segment separators,
        and calls the appropriate handler for each segment and resolver for resolving the group state
        based on the message type (e.g., APERAK, MSCONS, etc.).

        Args:
            edifact_text (str): The string content of the EDIFACT-specific message to parse
            max_lines_to_parse (int): The maximum number of lines to parse, defaults to -1 has no line-parsing limit

        Returns:
            EdifactInterchange: The parsed interchange object containing the structured content of the EDIFACT-specific message
        """
        if edifact_text is None:
            raise EdifactParserException("No valid parsing input. Input was", str(edifact_text))

        segment_types = [segment_type.value for segment_type in SegmentType]

        has_una_segment = self.__initialize_una_segment_logic_return_if_has_una_segment(edifact_text=edifact_text)
        interchange_cached = None
        if has_una_segment:
            interchange_cached = self.__context.interchange

        # Updates the parsing context by specifying the algorithm to be used for the message type to be parsed (e.g., APERAK, MSCONS, etc.).
        self.__context = ParsingContextFactory.identify_and_create_context(
            edifact_text=edifact_text, parsing_context=self.__context
        )
        if interchange_cached:
            self.__context.interchange = interchange_cached

        segments = self.__syntax_parser.split_segments(string_content=edifact_text, context=self.__context)
        amount_of_segments = len(segments)

        if amount_of_segments <= EdifactConstants.MIN_SEGMENT_COUNT_OF_AN_EDIFACT_MESSAGE:
            raise EdifactParserException("No valid parsing input. Input was", str(edifact_text))

        if (0 < max_lines_to_parse) and (max_lines_to_parse < amount_of_segments):
            raise EdifactParserException(
                f"Maximum number of segments reached (max: {max_lines_to_parse} less than number of segments: {amount_of_segments})")

        group_state_resolver = self.__resolver_factory.get_resolver(self.__context.message_type)

        last_segment_type: Optional[str] = None
        current_segment_group: Optional[str] = None
        for segment in segments:
            self.__context.segment_count += 1
            line_number = self.__context.segment_count

            segment_line = segment.strip()
            if not segment_line:
                continue
            if has_una_segment:
                # Reset back the flag to continue with other segments
                has_una_segment = False
                continue

            segment_line = self.__syntax_parser.remove_invalid_prefix_from_segment_data(
                string_content=segment_line,
                segment_types=segment_types,
                context=self.__context,
            )

            element_components = self.__syntax_parser.split_elements(
                string_content=segment_line,
                context=self.__context
            )
            if not element_components:
                continue
            segment_type_components = self.__syntax_parser.split_components(
                string_content=element_components[0],
                context=self.__context
            )
            if not segment_type_components:
                continue
            segment_type = segment_type_components[0]
            current_segment_group = group_state_resolver.resolve_and_get_segment_group(
                current_segment_type=segment_type,
                current_segment_group=current_segment_group,
                context=self.__context
            )

            segment_handler = self.__handler_factory.get_handler(segment_type)
            if segment_handler:
                # Use the dedicated handler
                segment_handler.handle(
                    line_number=line_number,
                    element_components=element_components,
                    last_segment_type=last_segment_type,
                    current_segment_group=current_segment_group,
                    context=self.__context
                )
            last_segment_type = segment_type

        return self.__context.interchange

    def __initialize_una_segment_logic_return_if_has_una_segment(self, edifact_text: str) -> bool:
        """
        Checks for UNA segment and initializes it if found.

        Args:
            edifact_text (str): The EDIFACT text to parse

        Returns:
            bool: True if UNA segment was found and initialized, False otherwise
        """
        una_segment = self.__syntax_parser.find_and_get_una_segment(edifact_text)
        if una_segment:
            self.__initialize_una_segment(una_segment)
            return True
        return False

    def __initialize_una_segment(self, una_segment: str) -> None:
        """
        Initializes the UNA segment by processing it with the appropriate handler.

        Args:
            una_segment (str): The UNA segment to initialize
        """
        # Process the UNA segment to set the delimiters
        una_handler = self.__handler_factory.get_handler(SegmentType.UNA)
        if una_handler:
            una_handler.handle(
                line_number=1,
                element_components=[una_segment],
                last_segment_type=None,
                current_segment_group=None,
                context=self.__context
            )
