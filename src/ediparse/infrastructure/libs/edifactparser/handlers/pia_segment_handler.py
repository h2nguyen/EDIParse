# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..converters import PIASegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentPIA


class PIASegmentHandler(SegmentHandler[SegmentPIA]):
    """
    Handler for PIA (Product Identification) segments.

    This handler processes PIA segments, which specify the product identification 
    for the current item using the OBIS identifier or the medium. It updates the 
    parsing context with the converted PIA segment information.

    Currently, this handler supports EDIFACT-specific messages, where PIA segments are used in
    segment group SG9 to provide product identification information.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the PIA segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(PIASegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentPIA, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted PIA segment.
        The update depends on the current segment group.

        Args:
            segment: The converted PIA segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG9 == current_segment_group:
            context.current_sg9.pia_produktidentifikation = segment
