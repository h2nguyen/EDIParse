# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import (
    SegmentPIA, WarenLeistungsnummerIdentifikation
)


class PIASegmentConverter(SegmentConverter[SegmentPIA]):
    """
    Converter for PIA (Product Identification) segments.

    This converter transforms PIA segment data from EDIFACT format into a structured
    SegmentPIA object. The PIA segment is used to specify the product identification 
    for the current item using the OBIS identifier or the medium.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the PIA segment converter with the syntax parser.

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
    ) -> SegmentPIA:
        """
        Converts PIA (Product identification) segment components to a SegmentPIA object.

        The PIA segment is used to specify the product identification for the current
        item using the OBIS identifier or the medium.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentPIA object with product identification qualifier, goods/service number
            identification and type of product/service code

        Examples:
        PIA+5+1-1?:1.8.1:SRW'
        PIA+5+1-1?:1.29.1:SRW' - Example of product identification using an OBIS code
        PIA+5+AUA:Z08' - Example of product identification using a medium
        """
        produkt_erzeugnisnummer_qualifier = element_components[1]
        waren_leistungsnummer_identifikation_details = self._syntax_parser.split_components(
            string_content=element_components[2],
            context=context,
            include_escape_symbol=False
        )
        produkt_leistungsnummer = waren_leistungsnummer_identifikation_details[0]
        art_der_produkt_leistungsnummer_code = waren_leistungsnummer_identifikation_details[1]

        return SegmentPIA(
            produkt_erzeugnisnummer_qualifier=produkt_erzeugnisnummer_qualifier,
            waren_leistungsnummer_identifikation=WarenLeistungsnummerIdentifikation(
                produkt_leistungsnummer=produkt_leistungsnummer,
                art_der_produkt_leistungsnummer_code=art_der_produkt_leistungsnummer_code
            )
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        pass
