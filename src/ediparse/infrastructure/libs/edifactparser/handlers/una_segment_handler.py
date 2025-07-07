# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..converters import UNASegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.constants import SegmentGroup
from ..wrappers.context import ParsingContext
from ..wrappers.segments import SegmentUNA


class UNASegmentHandler(SegmentHandler[SegmentUNA]):
    """
    Handler for UNA segments (Service String Advice).

    The UNA segment defines the special characters used as delimiters in the EDIFACT message.
    When present, it overrides the default delimiters defined by the EDIFACT standard.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the UNA segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(UNASegmentConverter(syntax_parser=syntax_parser))

    def can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.
        UNA segments can always be handled if the interchange exists.

        Args:
            context: The parsing context to check.

        Returns:
            True if the context is valid, False otherwise.
        """
        return context.interchange is not None

    def _update_context(self, segment: SegmentUNA, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted UNA segment.

        Args:
            segment: The converted UNA segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        # Store the UNA segment in the interchange
        context.interchange.una_service_string_advice = segment
