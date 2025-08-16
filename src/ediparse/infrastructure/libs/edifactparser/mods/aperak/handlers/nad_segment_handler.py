# coding: utf-8

from typing import Optional

from ....handlers.nad_segment_handler import NADSegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentNAD
from ..segments import (
    SegmentGroup3 as ApkSG3,
)


class APERAKNADSegmentHandler(NADSegmentHandler):
    """
    APERAK-specific handler for NAD (Name and Address) segments.

    This handler processes NAD segments in APERAK messages, which identify the market partners.
    It updates the parsing context with the converted NAD segment information, creating new
    segment groups as needed.

    In APERAK messages, NAD segments are used in segment group SG3.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the APERAK NAD segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper)

    def _update_context(self, segment: SegmentNAD, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted NAD segment for APERAK messages.
        The update depends on the current segment group.

        Args:
            segment: The converted NAD segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG3 == current_segment_group:
            context.current_sg3 = ApkSG3()
            context.current_sg3.nad_marktpartner = segment
            context.current_message.sg3_marktpartnern.append(context.current_sg3)
