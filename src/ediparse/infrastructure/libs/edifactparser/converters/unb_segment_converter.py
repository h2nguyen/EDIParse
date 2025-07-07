# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import (
    SyntaxBezeichner, Marktpartner, DatumUhrzeit, SegmentUNB
)


class UNBSegmentConverter(SegmentConverter[SegmentUNB]):
    """
    Converter for UNB (Interchange Header) segments.

    This converter transforms UNB segment data from EDIFACT format into a structured
    SegmentUNB object. The UNB segment identifies an interchange and contains the 
    sender and recipient identification, date and time of preparation, and interchange 
    control reference.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the UNB segment converter with the syntax parser.

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
    ) -> SegmentUNB:
        """
        Converts UNB (Interchange Header) segment components to a SegmentUNB object.

        The UNB segment identifies an interchange. It contains the sender and recipient identification, 
        date and time of preparation, and interchange control reference.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentUNB object with syntax identifier, sender, recipient, creation date/time, 
            data exchange reference, application reference, and test indicator

        Example:
        UNB+UNOC:3+4012345678901:14+4012345678901:14+200426:1151+ABC4711++TL++++1'
        """
        syntax_info = self._syntax_parser.split_components(
            string_content=element_components[1],
            context=context
        )

        absender_info = self._syntax_parser.split_components(
            string_content=element_components[2],
            context=context
        )

        empfaenger_info = self._syntax_parser.split_components(
            string_content=element_components[3],
            context=context
        )

        erstellung_info = self._syntax_parser.split_components(
            string_content=element_components[4],
            context=context
        )

        datenaustauschreferenz = self._syntax_parser.split_components(
            string_content=element_components[5],
            context=context
        )[0] if len(element_components) > 5 else None

        anwendungsreferenz = self._syntax_parser.split_components(
            string_content=element_components[7],
            context=context
        )[0] if len(element_components) > 7 else None

        test_kennzeichen = self._syntax_parser.split_components(
            string_content=element_components[11],
            context=context
        )[0] if len(element_components) > 11 else None

        return SegmentUNB(
            syntax_bezeichner=SyntaxBezeichner(
                syntax_kennung=syntax_info[0],
                syntax_versionsnummer=(syntax_info[1] if len(syntax_info) > 1 else None)
            ),
            absender_der_uebertragungsdatei=Marktpartner(
                marktpartneridentifikationsnummer=absender_info[0],
                teilnehmerbezeichnung_qualifier=absender_info[1]
            ),
            empfaenger_der_uebertragungsdatei=Marktpartner(
                marktpartneridentifikationsnummer=empfaenger_info[0],
                teilnehmerbezeichnung_qualifier=empfaenger_info[1]
            ),
            datum_uhrzeit_der_erstellung=DatumUhrzeit(
                datum=erstellung_info[0],
                uhrzeit=erstellung_info[1]
            ),
            datenaustauschreferenz=datenaustauschreferenz,
            anwendungsreferenz=anwendungsreferenz,
            test_kennzeichen=test_kennzeichen,
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        pass