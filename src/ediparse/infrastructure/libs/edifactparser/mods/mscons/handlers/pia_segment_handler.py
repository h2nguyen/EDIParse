# coding: utf-8

from typing import Optional

from ....handlers.pia_segment_handler import PIASegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentPIA


class MSCONSPIASegmentHandler(PIASegmentHandler):
    """
    MSCONS-specific handler for PIA (Product Identification) segments.

    This handler processes PIA segments in MSCONS messages, which specify the product identification 
    for the current item using the OBIS identifier or the medium. It updates the parsing context 
    with the converted PIA segment information.

    In MSCONS messages, PIA segments are used in segment group SG9 to provide product identification information.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the MSCONS PIA segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper)

    def _update_context(self, segment: SegmentPIA, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted PIA segment for MSCONS messages.
        The update depends on the current segment group.

        Args:
            segment: The converted PIA segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG9 == current_segment_group:
            context.current_sg9.pia_produktidentifikation = segment