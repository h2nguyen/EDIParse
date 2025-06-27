# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..converters import NADSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup, EdifactMessageType
from ..wrappers.segments import SegmentNAD
from ..mods.mscons.segments import (
    SegmentGroup2 as MscSG2, SegmentGroup5 as MscSG5
)
from ..mods.aperak.segments import (
    SegmentGroup3 as ApkSG3,
)


class NADSegmentHandler(SegmentHandler[SegmentNAD]):
    """
    Handler for NAD (Name and Address) segments.

    This handler processes NAD segments, which identify the market partners and 
    the delivery location. It updates the parsing context with the converted NAD 
    segment information, creating new segment groups as needed.

    Currently, this handler supports both MSCONS and APERAK messages:
    - In MSCONS messages, NAD segments are used in segment groups SG2 and SG5
    - In APERAK messages, NAD segments are used in segment group SG3
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the NAD segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(NADSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentNAD, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted NAD segment.
        The update depends on the current segment group.

        Args:
            segment: The converted NAD segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if EdifactMessageType.MSCONS == context.message_type:
            if SegmentGroup.SG2 == current_segment_group:
                context.current_sg2 = MscSG2()
                context.current_sg2.nad_marktpartner = segment
                context.current_message.sg2_marktpartnern.append(context.current_sg2)
            elif SegmentGroup.SG5 == current_segment_group:
                if not context.current_sg5:
                    context.current_sg5 = MscSG5()
                context.current_sg5.nad_name_und_adresse = segment
                context.current_message.sg5_liefer_bzw_bezugsorte.append(context.current_sg5)
        elif EdifactMessageType.APERAK == context.message_type:
            if SegmentGroup.SG3 == current_segment_group:
                context.current_sg3 = ApkSG3()
                context.current_sg3.nad_marktpartner = segment
                context.current_message.sg3_marktpartnern.append(context.current_sg3)
