# coding: utf-8

from typing import Optional

from ....converters.sts_segment_converter import STSSegmentConverter
from ....utils import EdifactSyntaxHelper
from ....wrappers.constants import SegmentGroup
from ....wrappers.context import ParsingContext


class MSCONSSTSSegmentConverter(STSSegmentConverter):
    """
    MSCONS-specific converter for STS (Status) segments.

    This converter transforms STS segment data from EDIFACT format into a structured
    SegmentSTS object for MSCONS messages. It provides MSCONS-specific mappings from
    status category codes to human-readable names.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the MSCONS STS segment converter with the syntax parser.

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
        Maps STS status category codes to human-readable identifier names for MSCONS messages.

        This method provides specific mappings for status category codes to meaningful
        names that describe the type of status information being provided in MSCONS messages.

        Args:
            qualifier_code: The status category code from the STS segment
            current_segment_group: The current segment group being processed
            context: The parsing context containing the message type and segment group context information

        Returns:
            A human-readable identifier name for the status category, or None if no mapping exists
        """
        if not qualifier_code:
            return None
        if qualifier_code == "10":
            return "Grundlage der Energiemenge"
        if qualifier_code == "Z31":
            return "Gasqualität"
        if qualifier_code == "Z32":
            return "Ersatzwertbildungsverfahren"
        if qualifier_code == "Z33":
            return "Plausibilisierungshinweis"
        if qualifier_code == "Z34":
            return "Korrekturgrund"
        if qualifier_code == "Z40":
            return "Grund der Ersatzwertbildung"
        return None