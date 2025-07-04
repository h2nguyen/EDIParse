# coding: utf-8

import logging
from typing import Optional

from . import SegmentHandler
from ..converters import DTMSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup, EdifactMessageType
from ..wrappers.segments import SegmentDTM

logger = logging.getLogger(__name__)


class DTMSegmentHandler(SegmentHandler[SegmentDTM]):
    """
    Handler for DTM (Date/Time/Period) segments.

    This handler processes DTM segments, which specify dates, times, periods, and their 
    function within the message. It updates the parsing context with the converted DTM 
    segment information, appending it to the appropriate collection based on the current 
    segment group.

    Currently, this handler supports both MSCONS and APERAK messages:
    - In MSCONS messages, DTM segments are used in the header and segment groups SG1, SG6, and SG10
    - In APERAK messages, DTM segments are used in the header and segment group SG2
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the DTM segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(DTMSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentDTM, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted DTM segment.
        The update depends on the current segment group.

        Args:
            segment: The converted DTM segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if EdifactMessageType.MSCONS == context.message_type:
            if current_segment_group is None:
                context.current_message.dtm_nachrichtendatum.append(segment)
            elif SegmentGroup.SG1 == current_segment_group:
                context.current_sg1.dtm_versionsangabe_marktlokationsscharfe_allokationsliste_gas_mmma.append(segment)
            elif SegmentGroup.SG6 == current_segment_group:
                context.current_sg6.dtm_zeitraeume.append(segment)
            elif SegmentGroup.SG10 == current_segment_group:
                context.current_sg10.dtm_zeitangaben.append(segment)
            else:
                # Unknown segment group
                logger.debug(f"Keine Behandlung für DTM-Segment '{segment}' definiert.")
        elif EdifactMessageType.APERAK == context.message_type:
            if current_segment_group is None:
                context.current_message.dtm_nachrichtendatum.append(segment)
            elif SegmentGroup.SG2 == current_segment_group:
                context.current_sg2.dtm_referenzdatum.append(segment)
            else:
                # Unknown segment group
                logger.debug(f"Keine Behandlung für DTM-Segment '{segment}' definiert.")
