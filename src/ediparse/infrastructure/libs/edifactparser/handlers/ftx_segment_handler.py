# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..converters.ftx_segment_converter import FTXSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.segments import SegmentFTX
from ..wrappers.constants import SegmentGroup
from ..wrappers.constants import EdifactMessageType


class FTXSegmentHandler(SegmentHandler[SegmentFTX]):
    """
    Handler for FTX (Free Text) segments.

    This handler processes FTX segments, which contain free-format text information.
    FTX segments are used to provide detailed descriptions or additional information
    in various message types. The handler updates the parsing context by adding the 
    segment to the appropriate segment group based on the message type.

    Currently, this handler supports APERAK messages, where FTX segments are used for
    error descriptions and acknowledgement information in segment groups SG4 and SG5.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the FTX segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(FTXSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentFTX, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted FTX segment.
        The update depends on the message type and current segment group.
        For APERAK messages, the segment is added to either SG4 or SG5.

        Args:
            segment: The converted FTX segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if EdifactMessageType.APERAK == context.message_type:
            if SegmentGroup.SG4 == current_segment_group:
                context.current_sg4.ftx_freier_text = segment
            elif SegmentGroup.SG5 == current_segment_group:
                context.current_sg5.ftx_referenz_texte.append(segment)
