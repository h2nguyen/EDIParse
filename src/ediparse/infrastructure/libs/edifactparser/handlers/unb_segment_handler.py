# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..utils import EdifactSyntaxHelper
from ..wrappers.constants import SegmentGroup
from ..wrappers.context import ParsingContext
from ..wrappers.segments import SegmentUNB


class UNBSegmentHandler(SegmentHandler[SegmentUNB]):
    """
    Handler for UNB (Interchange Header) segments.

    This handler processes UNB segments, which identify an interchange and contain 
    the sender and recipient identification, date and time of preparation, and 
    interchange control reference. It updates the parsing context with the converted 
    UNB segment information.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the UNB segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(
            syntax_helper=syntax_helper,
        )

    def can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.
        UNB segments can always be handled if the interchange exists.

        Args:
            context: The parsing context to check.

        Returns:
            True if the context is valid, False otherwise.
        """
        return context.interchange is not None

    def _update_context(self, segment: SegmentUNB, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted UNB segment.

        Args:
            segment: The converted UNB segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.interchange.unb_nutzdaten_kopfsegment = segment
