# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..converters import UNZSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.constants import SegmentGroup
from ..wrappers.context import ParsingContext
from ..wrappers.segments import SegmentUNZ


class UNZSegmentHandler(SegmentHandler[SegmentUNZ]):
    """
    Handler for UNZ (Interchange Trailer) segments.

    This handler processes UNZ segments, which are used to end and check the completeness 
    of an interchange. It updates the parsing context with the converted UNZ segment 
    information, which includes the count of messages in the interchange and the 
    interchange reference.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the UNZ segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(
            syntax_helper=syntax_helper,
            converter=UNZSegmentConverter(syntax_helper=syntax_helper)
        )

    def can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.
        UNZ segments can be handled if the interchange exists.

        Args:
            context: The parsing context to check.

        Returns:
            True if the context is valid, False otherwise.
        """
        return context.interchange is not None

    def _update_context(self, segment: SegmentUNZ, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted UNZ segment.

        Args:
            segment: The converted UNZ segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.interchange.unz_nutzdaten_endsegment = segment
