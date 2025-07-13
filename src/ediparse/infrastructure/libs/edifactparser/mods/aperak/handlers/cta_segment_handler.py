# coding: utf-8

from typing import Optional

from ....handlers.cta_segment_handler import CTASegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentCTA


class APERAKCTASegmentHandler(CTASegmentHandler):
    """
    APERAK-specific handler for CTA (Contact Information) segments.

    This handler processes CTA segments in APERAK messages, which identify a person or department 
    to whom communication should be directed. It updates the parsing context with the converted 
    CTA segment information, appending it to the appropriate segment group.

    In APERAK messages, CTA segments are used in segment group SG3.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the APERAK CTA segment handler with the appropriate __converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser)

    def _update_context(self, segment: SegmentCTA, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted CTA segment for APERAK messages.
        The update depends on the current segment group.

        Args:
            segment: The converted CTA segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG3 == current_segment_group:
            context.current_sg3.cta_ansprechpartnern.append(segment)