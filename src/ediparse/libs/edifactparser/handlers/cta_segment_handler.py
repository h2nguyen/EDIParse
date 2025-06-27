# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..converters import CTASegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup, EdifactMessageType
from ..wrappers.segments import SegmentCTA
from ..mods.mscons.segments import SegmentGroup4


class CTASegmentHandler(SegmentHandler[SegmentCTA]):
    """
    Handler for CTA (Contact Information) segments.

    This handler processes CTA segments, which identify a person or department to whom 
    communication should be directed. It updates the parsing context with the converted 
    CTA segment information, creating a new segment group 4 when needed.

    Currently, this handler supports both MSCONS and APERAK messages:
    - In MSCONS messages, CTA segments are used in segment group SG4
    - In APERAK messages, CTA segments are used in segment group SG3
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the CTA segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(CTASegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentCTA, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted CTA segment.
        The update depends on the current segment group.

        Args:
            segment: The converted CTA segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if EdifactMessageType.MSCONS == context.message_type:
            if SegmentGroup.SG4 == current_segment_group:
                context.current_sg4 = SegmentGroup4()
                context.current_sg4.cta_ansprechpartner = segment
                context.current_sg2.sg4_kontaktinformationen.append(context.current_sg4)
        elif EdifactMessageType.APERAK == context.message_type:
            if SegmentGroup.SG3 == current_segment_group:
                context.current_sg3.cta_ansprechpartnern.append(segment)
