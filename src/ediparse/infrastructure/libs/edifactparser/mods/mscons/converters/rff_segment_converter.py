# coding: utf-8

from typing import Optional

from ....converters.rff_segment_converter import RFFSegmentConverter
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup


class MSCONSRFFSegmentConverter(RFFSegmentConverter):
    """
    MSCONS-specific __converter for RFF (Reference) segments.

    This __converter transforms RFF segment data from EDIFACT format into a structured
    SegmentRFF object for MSCONS messages. It provides MSCONS-specific mappings from
    qualifier codes to human-readable names.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the MSCONS RFF segment __converter with the syntax parser.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper=syntax_helper)

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        """
        Maps RFF qualifier codes to human-readable identifier names for MSCONS messages.

        This method provides specific mappings for reference qualifier codes to meaningful
        names that describe their purpose in MSCONS messages, taking into account the current
        segment group context.

        Args:
            qualifier_code: The reference qualifier code from the RFF segment
            current_segment_group: The current segment group being processed
            context: The parsing context containing the message type and segment group context information

        Returns:
            A human-readable identifier name for the reference, or None if no mapping exists
        """
        if qualifier_code == "AGI":
            return "Beantragungsnummer"
        if qualifier_code == "AGK":
            return "Anwendungsreferenznummer"
        if qualifier_code == "MG":
            return "Gerätenummer"
        if qualifier_code == "Z13":
            return "Prüfidentifikator"
        if qualifier_code == "Z30":
            return "Referenz auf vorherige Stammdatenmeldung des MSB"

        return super()._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=context
        )
