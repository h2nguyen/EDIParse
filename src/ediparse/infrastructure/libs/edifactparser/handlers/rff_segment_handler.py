# coding: utf-8

import logging
from typing import Optional

from . import SegmentHandler
from ..converters import RFFSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup, EdifactMessageType
from ..wrappers.segments import SegmentRFF
from ..mods.mscons.segments import (
    SegmentGroup1 as MscSG1, SegmentGroup7 as MscSG7
)
from ..mods.aperak.segments import (
    SegmentGroup2 as ApkSG2, SegmentGroup5 as ApkSG5
)

logger = logging.getLogger(__name__)


class RFFSegmentHandler(SegmentHandler[SegmentRFF]):
    """
    Handler for RFF (Reference) segments.

    This handler processes RFF segments, which specify reference information, such as 
    verification identifier, configuration ID, device number, or previous master data 
    message of the Metering Point Operator (MSB). It updates the parsing context with 
    the converted RFF segment information, creating new segment groups as needed.

    Currently, this handler supports both MSCONS and APERAK messages:
    - In MSCONS messages, RFF segments are used in segment groups SG1 and SG7
    - In APERAK messages, RFF segments are used in segment groups SG2 and SG5
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the RFF segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(RFFSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentRFF, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted RFF segment.
        The update depends on the current segment group.

        Args:
            segment: The converted RFF segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """

        if EdifactMessageType.MSCONS == context.message_type:
            if SegmentGroup.SG1 == current_segment_group:
                context.current_sg1 = MscSG1()
                context.current_sg1.rff_referenzangaben = segment
                context.current_message.sg1_referenzen.append(context.current_sg1)
            elif SegmentGroup.SG7 == current_segment_group:
                context.current_sg7 = MscSG7()
                context.current_sg7.rff_referenzangabe = segment
                context.current_sg6.sg7_referenzangaben.append(context.current_sg7)
        elif EdifactMessageType.APERAK == context.message_type:
            if SegmentGroup.SG2 == current_segment_group:
                context.current_sg2 = ApkSG2()
                context.current_sg2.rff_referenzangaben = segment
                context.current_message.sg2_referenzen.append(context.current_sg2)
            elif SegmentGroup.SG5 == current_segment_group:
                context.current_sg5 = ApkSG5()
                context.current_sg5.rff_referenz = segment
                context.current_sg4.sg5_nachrichtenreferenzen.append(context.current_sg5)
