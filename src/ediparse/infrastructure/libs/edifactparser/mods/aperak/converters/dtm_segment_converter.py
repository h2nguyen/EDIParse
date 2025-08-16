# coding: utf-8

from typing import Optional

from ....converters.dtm_segment_converter import DTMSegmentConverter
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup


class APERAKDTMSegmentConverter(DTMSegmentConverter):
    """
    APERAK-specific __converter for DTM (Date/Time/Period) segments.

    This __converter transforms DTM segment data from EDIFACT format into a structured
    SegmentDTM object for APERAK messages. It provides APERAK-specific mappings from
    qualifier codes to human-readable names.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the APERAK DTM segment __converter with the syntax parser.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper=syntax_helper)

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        """
        Maps DTM qualifier codes to human-readable identifier names for APERAK messages.

        This method provides specific mappings for date/time function qualifiers to meaningful
        names that describe their purpose in APERAK messages, taking into account the current
        segment group context.

        Args:
            qualifier_code: The date/time function qualifier code from the DTM segment
            current_segment_group: The current segment group being processed
            context: The parsing context containing the message type and segment group context information

        Returns:
            A human-readable identifier name for the date/time function, or None if no mapping exists
        """
        if qualifier_code == "137":
            return "Dokumenten-/Nachrichtendatum/-zeit"
        if qualifier_code == "171":
            return "Referenzdatum/-zeit"
        return super()._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=context
        )
