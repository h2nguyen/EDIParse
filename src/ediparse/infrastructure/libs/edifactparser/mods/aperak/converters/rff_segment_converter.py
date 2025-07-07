# coding: utf-8

from typing import Optional

from ....converters.rff_segment_converter import RFFSegmentConverter
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup


class APERAKRFFSegmentConverter(RFFSegmentConverter):
    """
    APERAK-specific converter for RFF (Reference) segments.

    This converter transforms RFF segment data from EDIFACT format into a structured
    SegmentRFF object for APERAK messages. It provides APERAK-specific mappings from
    qualifier codes to human-readable names.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the APERAK RFF segment converter with the syntax parser.

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
        Maps RFF qualifier codes to human-readable identifier names for APERAK messages.

        This method provides specific mappings for reference qualifier codes to meaningful
        names that describe their purpose in APERAK messages, taking into account the current
        segment group context.

        Args:
            qualifier_code: The reference qualifier code from the RFF segment
            current_segment_group: The current segment group being processed
            context: The parsing context containing the message type and segment group context information

        Returns:
            A human-readable identifier name for the reference, or None if no mapping exists
        """
        if not qualifier_code:
            return None
        if qualifier_code in ["ACE", "AGI"]:
            return "Referenzangaben"
        if qualifier_code == "ACW":
            return "Referenznummer der Nachricht"
        if qualifier_code == "AGO":
            return "Dokumentennummer der referenzierten Nachricht"
        if qualifier_code == "TN":
            return "Referenznummer des Vorgangs"
        if qualifier_code == "Z08":
            return "Netzbetreiber"

        return None
