# coding: utf-8
from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentDTM


class DTMSegmentConverter(SegmentConverter[SegmentDTM]):
    """
    Abstract __converter for DTM (Date/Time/Period) segments.

    This __converter transforms DTM segment data from EDIFACT format into a structured
    SegmentDTM object. The DTM segment specifies dates, times, periods, and their 
    function within the message.

    Specific implementations for different message types (e.g., MSCONS, APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the DTM segment __converter with the syntax parser.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper=syntax_helper)

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> SegmentDTM:
        """
        Converts DTM (Date/Time/Period) segment components to a SegmentDTM object.

        The DTM segment specifies dates, times, periods, and their function within the message.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the __converter.

        Returns:
            SegmentDTM object with date/time function qualifier, value, and format code

        Examples:
        DTM+137:202106011315?+00:303'
        DTM+157:202002:610'
        DTM+163:202102012300?+00:303'
        DTM+164:202102022300?+00:303'
        DTM+293:20210420103245?+00:304'
        DTM+492:202004:610'
        """
        details = self._syntax_parser.split_components(
            string_content=element_components[1],
            context=context,
            include_escape_symbol=False
        )
        datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier = details[0]
        datum_oder_uhrzeit_oder_zeitspanne_wert = details[1] if len(details) > 1 else None
        datums_oder_uhrzeit_oder_zeitspannen_format_code = details[2] if len(details) > 2 else None

        return SegmentDTM(
            bezeichner=self._get_identifier_name(
                qualifier_code=datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier,
                current_segment_group=current_segment_group,
                context=context
            ),
            datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier=datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier,
            datum_oder_uhrzeit_oder_zeitspanne_wert=datum_oder_uhrzeit_oder_zeitspanne_wert,
            datums_oder_uhrzeit_oder_zeitspannen_format_code=datums_oder_uhrzeit_oder_zeitspannen_format_code
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        """
        Maps DTM qualifier codes to human-readable identifier names.

        This method provides specific mappings for date/time function qualifiers to meaningful
        names that describe their purpose in EDIFACT messages, taking into account the current
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

        return super()._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=context
        )
