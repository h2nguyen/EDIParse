# coding: utf-8

import logging
from typing import Optional

from ....handlers.dtm_segment_handler import DTMSegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentDTM

logger = logging.getLogger(__name__)


class APERAKDTMSegmentHandler(DTMSegmentHandler):
    """
    APERAK-specific handler for DTM (Date/Time/Period) segments.

    This handler processes DTM segments in APERAK messages, which specify dates, times, periods, 
    and their function within the message. It updates the parsing context with the converted DTM 
    segment information, appending it to the appropriate collection based on the current segment group.

    In APERAK messages, DTM segments are used in the header and segment group SG2.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the APERAK DTM segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser)

    def _update_context(self, segment: SegmentDTM, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted DTM segment for APERAK messages.
        The update depends on the current segment group.

        Args:
            segment: The converted DTM segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if current_segment_group is None:
            context.current_message.dtm_nachrichtendatum.append(segment)
        elif SegmentGroup.SG2 == current_segment_group:
            context.current_sg2.dtm_referenzdatum.append(segment)
        else:
            # Unknown segment group
            logger.debug(f"Keine Behandlung für DTM-Segment '{segment}' definiert.")