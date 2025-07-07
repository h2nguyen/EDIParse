# coding: utf-8

from typing import Optional

from ....converters.dtm_segment_converter import DTMSegmentConverter
from ....utils import EdifactSyntaxHelper
from ....wrappers.constants import SegmentGroup
from ....wrappers.context import ParsingContext


class MSCONSDTMSegmentConverter(DTMSegmentConverter):
    """
    MSCONS-specific converter for DTM (Date/Time/Period) segments.

    This converter transforms DTM segment data from EDIFACT format into a structured
    SegmentDTM object for MSCONS messages. It provides MSCONS-specific mappings from
    qualifier codes to human-readable names.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the MSCONS DTM segment converter with the syntax parser.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser=syntax_parser)

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        """
        Maps DTM qualifier codes to human-readable identifier names for MSCONS messages.

        This method provides specific mappings for date/time function qualifiers to meaningful
        names that describe their purpose in MSCONS messages, taking into account the current
        segment group context.

        Args:
            qualifier_code: The date/time function qualifier code from the DTM segment
            current_segment_group: The current segment group being processed
            context: The parsing context containing the message type and segment group context information

        Returns:
            A human-readable identifier name for the date/time function, or None if no mapping exists
        """
        if not qualifier_code:
            return None
        elif qualifier_code == "7":
            if current_segment_group == SegmentGroup.SG10:
                return "Nutzungszeitpunkt"
        elif qualifier_code == "9":
            if current_segment_group == SegmentGroup.SG10:
                return "Ablesedatum"
        elif qualifier_code == "60":
            if current_segment_group == SegmentGroup.SG10:
                return "Ausführungs- / Änderungszeitpunkt"
        elif qualifier_code == "137":
            return "Nachrichtendatum"
        elif qualifier_code == "157":
            if current_segment_group == SegmentGroup.SG6:
                return "Gültigkeit, Beginndatum Profilschar"
        elif qualifier_code == "163":
            if current_segment_group == SegmentGroup.SG6:
                return "Beginn Messperiode Übertragungszeitraum"
            elif current_segment_group == SegmentGroup.SG10:
                return "Beginn Messperiode"
        elif qualifier_code == "164":
            if current_segment_group == SegmentGroup.SG6:
                return "Ende Messperiode Übertragungszeitraum"
            elif current_segment_group == SegmentGroup.SG10:
                return "Ende Messperiode"
        elif qualifier_code == "293":
            if current_segment_group == SegmentGroup.SG1:
                return "Versionsangabe marktlokationsscharfe Allokationsliste Gas (MMMA)"
            if current_segment_group == SegmentGroup.SG6:
                return "Versionsangabe"
        elif qualifier_code == "306":
            if current_segment_group == SegmentGroup.SG10:
                return "Leistungsperiode"
        elif qualifier_code == "492":
            if current_segment_group == SegmentGroup.SG6:
                return "Bilanzierungsmonat"

        return None