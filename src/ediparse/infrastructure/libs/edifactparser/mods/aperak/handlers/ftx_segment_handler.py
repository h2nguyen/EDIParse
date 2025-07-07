# coding: utf-8

from typing import Optional

from ....handlers.ftx_segment_handler import FTXSegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentFTX


class APERAKFTXSegmentHandler(FTXSegmentHandler):
    """
    APERAK-specific handler for FTX (Free Text) segments.

    This handler processes FTX segments in APERAK messages, which contain free-format text information.
    FTX segments are used to provide detailed descriptions or additional information.
    The handler updates the parsing context by adding the segment to the appropriate segment group.

    In APERAK messages, FTX segments are used for error descriptions and acknowledgement information
    in segment groups SG4 and SG5.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the APERAK FTX segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser)

    def _update_context(self, segment: SegmentFTX, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted FTX segment for APERAK messages.
        The update depends on the current segment group.

        Args:
            segment: The converted FTX segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG4 == current_segment_group:
            context.current_sg4.ftx_freier_text = segment
        elif SegmentGroup.SG5 == current_segment_group:
            context.current_sg5.ftx_referenz_texte.append(segment)