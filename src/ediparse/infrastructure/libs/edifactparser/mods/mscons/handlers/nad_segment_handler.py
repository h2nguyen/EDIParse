# coding: utf-8

from typing import Optional

from ..segments import (
    SegmentGroup2 as MscSG2, SegmentGroup5 as MscSG5
)
from ....handlers.nad_segment_handler import NADSegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.constants import SegmentGroup
from ....wrappers.context import ParsingContext
from ....wrappers.segments import SegmentNAD


class MSCONSNADSegmentHandler(NADSegmentHandler):
    """
    MSCONS-specific handler for NAD (Name and Address) segments.

    This handler processes NAD segments in MSCONS messages, which identify the market partners and 
    the delivery location. It updates the parsing context with the converted NAD segment information, 
    creating new segment groups as needed.

    In MSCONS messages, NAD segments are used in segment groups SG2 and SG5.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the MSCONS NAD segment handler with the MSCONS-specific NAD __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper)

    def _update_context(self, segment: SegmentNAD, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted NAD segment for MSCONS messages.
        The update depends on the current segment group.

        Args:
            segment: The converted NAD segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG2 == current_segment_group:
            context.current_sg2 = MscSG2()
            context.current_sg2.nad_marktpartner = segment
            context.current_message.sg2_marktpartnern.append(context.current_sg2)
        elif SegmentGroup.SG5 == current_segment_group:
            if not context.current_sg5:
                context.current_sg5 = MscSG5()
            context.current_sg5.nad_name_und_adresse = segment
            context.current_message.sg5_liefer_bzw_bezugsorte.append(context.current_sg5)
