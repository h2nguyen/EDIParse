# coding: utf-8

from typing import Optional

from ....handlers.rff_segment_handler import RFFSegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentRFF
from ..converters.rff_segment_converter import MSCONSRFFSegmentConverter
from ..segments import (
    SegmentGroup1 as MscSG1, SegmentGroup7 as MscSG7
)


class MSCONSRFFSegmentHandler(RFFSegmentHandler):
    """
    MSCONS-specific handler for RFF (Reference) segments.

    This handler processes RFF segments in MSCONS messages, which specify reference information, 
    such as verification identifier, configuration ID, device number, or previous master data 
    message of the Metering Point Operator (MSB). It updates the parsing context with the 
    converted RFF segment information, creating new segment groups as needed.

    In MSCONS messages, RFF segments are used in segment groups SG1 and SG7.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the MSCONS RFF segment handler with the MSCONS-specific RFF converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        # Initialize the parent class
        super().__init__(syntax_parser)
        # Set the converter to the MSCONS-specific RFF converter
        self.converter = MSCONSRFFSegmentConverter(syntax_parser)

    def _update_context(self, segment: SegmentRFF, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted RFF segment for MSCONS messages.
        The update depends on the current segment group.

        Args:
            segment: The converted RFF segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG1 == current_segment_group:
            context.current_sg1 = MscSG1()
            context.current_sg1.rff_referenzangaben = segment
            context.current_message.sg1_referenzen.append(context.current_sg1)
        elif SegmentGroup.SG7 == current_segment_group:
            context.current_sg7 = MscSG7()
            context.current_sg7.rff_referenzangabe = segment
            context.current_sg6.sg7_referenzangaben.append(context.current_sg7)
