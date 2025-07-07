# coding: utf-8

from typing import Optional

from ....handlers.cci_segment_handler import CCISegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentCCI
from ..segments import SegmentGroup8


class MSCONSCCISegmentHandler(CCISegmentHandler):
    """
    MSCONS-specific handler for CCI (Characteristic/Class ID) segments.

    This handler processes CCI segments in MSCONS messages, which specify product characteristics
    and the data that defines those characteristics. It updates the parsing context
    with the converted CCI segment information, creating a new segment group 8 when needed.

    In MSCONS messages, CCI segments are used in segment group SG8 to provide time series type information.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the MSCONS CCI segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser)

    def _update_context(self, segment: SegmentCCI, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted CCI segment for MSCONS messages.
        The update depends on the current segment group.

        Args:
            segment: The converted CCI segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG8 == current_segment_group:
            context.current_sg8 = SegmentGroup8()
            context.current_sg8.cci_zeitreihentyp = segment
            context.current_sg6.sg8_zeitreihentypen.append(context.current_sg8)