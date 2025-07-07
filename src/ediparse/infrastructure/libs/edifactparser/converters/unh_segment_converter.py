# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentUNH, NachrichtenKennung, StatusDerUebermittlung


class UNHSegmentConverter(SegmentConverter[SegmentUNH]):
    """
    Converter for UNH (Message Header) segments.

    This converter transforms UNH segment data from EDIFACT format into a structured
    SegmentUNH object. The UNH segment is used to head, identify, and specify a message,
    containing the message reference number, message type identifier, and transmission status.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the UNH segment converter with the syntax parser.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser=syntax_parser)

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> SegmentUNH:
        """
        Converts UNH (Message Header) segment components to a SegmentUNH object.

        The UNH segment is used to head, identify, and specify a message. It contains
        the message reference number, message type identifier, and transmission status.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentUNH object with message reference number, message identifier, 
            general assignment reference, and transmission status

        Examples:
        UNH+4+MSCONS:D:04B:UN:2.4c'
        UNH+1+MSCONS:D:04B:UN:2.4c+UNB_DE0020_nr_1+1:C' - Example for market location-specific allocation list for gas
        """
        nachrichten_referenz_info = element_components[1]
        nachrichten_kennung_details = self._syntax_parser.split_components(
            string_content=element_components[2],
            context=context,
            include_escape_symbol=False
        )
        allgemeine_zuordnungsreferenz = element_components[3] \
            if len(element_components) > 3 and len(element_components[3]) > 0 else None
        status_der_uebermittlung_details = self._syntax_parser.split_components(
            string_content=element_components[4],
            context=context,
            include_escape_symbol=False
        ) if len(element_components) > 4 else None

        return SegmentUNH(
            nachrichten_referenznummer=nachrichten_referenz_info,
            nachrichten_kennung=NachrichtenKennung(
                nachrichtentyp_kennung=nachrichten_kennung_details[0],
                versionsnummer_des_nachrichtentyps=nachrichten_kennung_details[1],
                freigabenummer_des_nachrichtentyps=nachrichten_kennung_details[2],
                verwaltende_organisation=nachrichten_kennung_details[3],
                anwendungscode_der_zustaendigen_organisation=nachrichten_kennung_details[4],
            ),
            allgemeine_zuordnungsreferenz=allgemeine_zuordnungsreferenz if allgemeine_zuordnungsreferenz else None,
            status_der_uebermittlung=StatusDerUebermittlung(
                uebermittlungsfolgenummer=status_der_uebermittlung_details[0],
                erste_und_letzte_uebermittlung=status_der_uebermittlung_details[1]
            ) if status_der_uebermittlung_details else None
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        pass
