# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import (
    SegmentCOM, Kommunikationsverbindung
)


class COMSegmentConverter(SegmentConverter[SegmentCOM]):
    """
    Converter for COM (Communication Contact) segments.

    This __converter transforms COM segment data from EDIFACT format into a structured
    SegmentCOM object. The COM segment provides communication information such as 
    telephone numbers, email addresses, etc.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the COM segment __converter with the syntax parser.

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
    ) -> SegmentCOM:
        """
        Converts COM (Communication Contact) segment components to a SegmentCOM object.

        The COM segment provides communication information such as telephone numbers, email addresses, etc.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the __converter.

        Returns:
            SegmentCOM object with communication connection details

        Examples:
        COM+?+3222271020:TE'
        COM+email@example.com:EM
        """
        kommunikationsverbindung = self._syntax_parser.split_components(
            string_content=element_components[1],
            context=context,
            include_escape_symbol=False
        )

        return SegmentCOM(
            kommunikationsverbindung=Kommunikationsverbindung(
                kommunikationsadresse_identifikation=kommunikationsverbindung[0],
                kommunikationsadresse_qualifier=kommunikationsverbindung[1] if len(
                    kommunikationsverbindung) > 1 else None
            )
        )
