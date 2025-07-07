# coding: utf-8

from typing import Optional

from ....handlers.rff_segment_handler import RFFSegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentRFF
from ..converters.rff_segment_converter import APERAKRFFSegmentConverter
from ..segments import (
    SegmentGroup2 as ApkSG2, SegmentGroup5 as ApkSG5
)


class APERAKRFFSegmentHandler(RFFSegmentHandler):
    """
    APERAK-specific handler for RFF (Reference) segments.

    This handler processes RFF segments in APERAK messages, which specify reference information.
    It updates the parsing context with the converted RFF segment information, creating new
    segment groups as needed.

    In APERAK messages, RFF segments are used in segment groups SG2 and SG5.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the APERAK RFF segment handler with the APERAK-specific RFF converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        # Initialize the parent class
        super().__init__(syntax_parser)
        # Set the converter to the APERAK-specific RFF converter
        self.converter = APERAKRFFSegmentConverter(syntax_parser)

    def _update_context(self, segment: SegmentRFF, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted RFF segment for APERAK messages.
        The update depends on the current segment group.

        Args:
            segment: The converted RFF segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG2 == current_segment_group:
            context.current_sg2 = ApkSG2()
            context.current_sg2.rff_referenzangaben = segment
            context.current_message.sg2_referenzen.append(context.current_sg2)
        elif SegmentGroup.SG5 == current_segment_group:
            context.current_sg5 = ApkSG5()
            context.current_sg5.rff_referenz = segment
            context.current_sg4.sg5_nachrichtenreferenzen.append(context.current_sg5)
