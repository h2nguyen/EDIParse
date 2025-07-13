# coding: utf-8

from typing import Optional

from ....handlers.cta_segment_handler import CTASegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentCTA
from ..segments import SegmentGroup4


class MSCONSCTASegmentHandler(CTASegmentHandler):
    """
    MSCONS-specific handler for CTA (Contact Information) segments.

    This handler processes CTA segments in MSCONS messages, which identify a person or department 
    to whom communication should be directed. It updates the parsing context with the converted 
    CTA segment information, creating a new segment group 4 when needed.

    In MSCONS messages, CTA segments are used in segment group SG4.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the MSCONS CTA segment handler with the appropriate __converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser)

    def _update_context(self, segment: SegmentCTA, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted CTA segment for MSCONS messages.
        The update depends on the current segment group.

        Args:
            segment: The converted CTA segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG4 == current_segment_group:
            context.current_sg4 = SegmentGroup4()
            context.current_sg4.cta_ansprechpartner = segment
            context.current_sg2.sg4_kontaktinformationen.append(context.current_sg4)