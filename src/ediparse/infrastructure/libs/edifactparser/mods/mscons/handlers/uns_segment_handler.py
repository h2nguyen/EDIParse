# coding: utf-8

from typing import Optional

from ....handlers.uns_segment_handler import UNSSegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentUNS


class MSCONSUNSSegmentHandler(UNSSegmentHandler):
    """
    MSCONS-specific handler for UNS (Section Control) segments.

    This handler processes UNS segments in MSCONS messages, which are used to separate the header and 
    detail sections of a message. It updates the parsing context with the converted UNS segment 
    information.

    In MSCONS messages, UNS segments are used to mark the transition from the header to the detail section.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the MSCONS UNS segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper)

    def _update_context(self, segment: SegmentUNS, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted UNS segment for MSCONS messages.

        Args:
            segment: The converted UNS segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.current_message.uns_abschnitts_kontrollsegment = segment