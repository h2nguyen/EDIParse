# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import (
    SegmentCTA, AbteilungOderBearbeiter
)


class CTASegmentConverter(SegmentConverter[SegmentCTA]):
    """
    Converter for CTA (Contact Information) segments.

    This converter transforms CTA segment data from EDIFACT format into a structured
    SegmentCTA object. The CTA segment identifies a person or department to whom 
    communication should be directed.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the CTA segment converter with the syntax parser.

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
    ) -> SegmentCTA:
        """
        Converts CTA (Contact Information) segment components to a SegmentCTA object.

        The CTA segment identifies a person or department to whom communication should be directed.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentCTA object with contact function code and department or employee information

        Example:
        CTA+IC+:P GETTY'
        """
        funktion_des_ansprechpartners_code = element_components[1]
        abteilung_oder_bearbeiter = self._syntax_parser.split_components(
            string_content=element_components[2],
            context=context,
            include_escape_symbol=False
        ) if len(element_components) > 2 else None

        return SegmentCTA(
            funktion_des_ansprechpartners_code=funktion_des_ansprechpartners_code,
            abteilung_oder_bearbeiter=AbteilungOderBearbeiter(
                abteilung_oder_bearbeiter=abteilung_oder_bearbeiter[1]
            ) if abteilung_oder_bearbeiter is not None and len(abteilung_oder_bearbeiter) > 1 else None
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        pass
