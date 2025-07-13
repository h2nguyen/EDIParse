# coding: utf-8

from typing import Optional

from ....handlers.qty_segment_handler import QTYSegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentQTY
from ..segments import SegmentGroup10


class MSCONSQTYSegmentHandler(QTYSegmentHandler):
    """
    MSCONS-specific handler for QTY (Quantity) segments.

    This handler processes QTY segments in MSCONS messages, which specify quantities for the current 
    item position, including the quantity value and unit of measurement. It updates the parsing context 
    with the converted QTY segment information, creating a new segment group 10 when needed.

    In MSCONS messages, QTY segments are used in segment group SG10 to provide quantity information.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the MSCONS QTY segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper)

    def _update_context(self, segment: SegmentQTY, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted QTY segment for MSCONS messages.
        The update depends on the current segment group.

        Args:
            segment: The converted QTY segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG10 == current_segment_group:
            context.current_sg10 = SegmentGroup10()
            context.current_sg10.qty_mengenangaben = segment
            context.current_sg9.sg10_mengen_und_statusangaben.append(context.current_sg10)