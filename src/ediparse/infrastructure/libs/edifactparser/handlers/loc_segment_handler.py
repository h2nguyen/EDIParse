# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..converters import LOCSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentLOC
from ..mods.mscons.segments import SegmentGroup6


class LOCSegmentHandler(SegmentHandler[SegmentLOC]):
    """
    Handler for LOC (Location) segments.

    This handler processes LOC segments, which specify the identification to which 
    the data applies and when EEG transfer time series are transferred. It updates 
    the parsing context with the converted LOC segment information, creating or 
    updating segment group 6 as needed.

    Currently, this handler supports EDIFACT-specific messages, where LOC segments are used in
    segment group SG6 to provide location identification information.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the LOC segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(LOCSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentLOC, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted LOC segment.
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
