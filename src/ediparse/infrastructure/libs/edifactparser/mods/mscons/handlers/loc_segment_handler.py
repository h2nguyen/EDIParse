# coding: utf-8

from typing import Optional

from ....handlers.loc_segment_handler import LOCSegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentLOC
from ..segments import SegmentGroup6


class MSCONSLOCSegmentHandler(LOCSegmentHandler):
    """
    MSCONS-specific handler for LOC (Location) segments.

    This handler processes LOC segments in MSCONS messages, which specify the identification to which 
    the data applies and when EEG transfer time series are transferred. It updates the parsing context 
    with the converted LOC segment information, creating or updating segment group 6 as needed.

    In MSCONS messages, LOC segments are used in segment group SG6 to provide location identification information.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the MSCONS LOC segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper)

    def _update_context(self, segment: SegmentLOC, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted LOC segment for MSCONS messages.
        The update depends on the current segment group.

        Args:
            segment: The converted LOC segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG6 == current_segment_group:
            if not context.current_sg6:
                context.current_sg6 = SegmentGroup6()
            context.current_sg6.loc_identifikationsangabe = segment
            context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt.append(context.current_sg6)