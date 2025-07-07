# coding: utf-8

from typing import Optional

from ....converters.nad_segment_converter import NADSegmentConverter
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup


class APERAKNADSegmentConverter(NADSegmentConverter):
    """
    APERAK-specific converter for NAD (Name and Address) segments.

    This converter transforms NAD segment data from EDIFACT format into a structured
    SegmentNAD object for APERAK messages. It provides APERAK-specific mappings from
    qualifier codes to human-readable names.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the APERAK NAD segment converter with the syntax parser.

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
        Maps NAD qualifier codes to human-readable identifier names for APERAK messages.

        This method provides specific mappings for NAD party qualifier codes to meaningful
        names that describe the role of the party in APERAK messages.

        Args:
            qualifier_code: The party qualifier code from the NAD segment
            current_segment_group: The current segment group being processed
            context: The parsing context containing the message type and segment group context information

        Returns:
            A human-readable identifier name for the party role, or None if no mapping exists
        """
        if not qualifier_code:
            return None
        if qualifier_code in ["DP", "DED", "Z15"]:
            return "Name und Adresse"
        if qualifier_code == "MR":
            return "MP-ID Empfänger"
        if qualifier_code == "MS":
            return "MP-ID Absender"
        return None