# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..converters import LINSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentLIN
from ..mods.mscons.segments import SegmentGroup9


class LINSegmentHandler(SegmentHandler[SegmentLIN]):
    """
    Handler for LIN (Line Item) segments.

    This handler processes LIN segments, which identify a line item and its configuration 
    in a message. It updates the parsing context with the converted LIN segment information, 
    creating a new segment group 9 when needed.

    Currently, this handler supports EDIFACT-specific messages, where LIN segments are used in
    segment group SG9 to provide line item information.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the LIN segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(LINSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentLIN, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted LIN segment.
        The update depends on the current segment group.

        Args:
            segment: The converted LIN segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG9 == current_segment_group:
            context.current_sg9 = SegmentGroup9()
            context.current_sg9.lin_lfd_position = segment
            context.current_sg6.sg9_positionsdaten.append(context.current_sg9)
