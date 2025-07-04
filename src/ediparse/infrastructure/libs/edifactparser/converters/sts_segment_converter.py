# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import (
    SegmentSTS, Statusanlass, Status, Statuskategorie
)


class STSSegmentConverter(SegmentConverter[SegmentSTS]):
    """
    Converter for STS (Status) segments.

    This converter transforms STS segment data from EDIFACT format into a structured
    SegmentSTS object. The STS segment is used to specify status information such as 
    correction reason, gas quality, replacement value formation procedure, or 
    plausibility note.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the STS segment converter with the syntax parser.

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
    ) -> SegmentSTS:
        """
        Converts STS (Status) segment components to a SegmentSTS object.

        The STS segment is used to specify status information such as correction reason, 
        gas quality, replacement value formation procedure, or plausibility note.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentSTS object with status category, status code, and status reason

        Examples:
        STS+Z34++Z81'
        STS+Z40++Z74'
        """

        statuskategorie_code = element_components[1]
        status_code = element_components[2] if len(element_components) > 2 else None
        statusanlass_code = element_components[3] if len(element_components) > 3 else None

        return SegmentSTS(
            bezeichner=self._get_identifier_name(
                qualifier_code=element_components[1],
                current_segment_group=current_segment_group,
                context=context
            ),
            statuskategorie=Statuskategorie(
                statuskategorie_code=statuskategorie_code
            ) if statuskategorie_code else None,
            status=Status(
                status_code=status_code
            ) if status_code else None,
            statusanlass=Statusanlass(
                statusanlass_code=statusanlass_code
            ) if statusanlass_code else None
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        """
        Maps STS status category codes to human-readable identifier names.

        This method provides specific mappings for status category codes to meaningful
        names that describe the type of status information being provided.

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
