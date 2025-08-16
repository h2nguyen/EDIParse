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
    Abstract __converter for STS (Status) segments.

    This __converter transforms STS segment data from EDIFACT format into a structured
    SegmentSTS object. The STS segment is used to specify status information such as 
    correction reason, gas quality, replacement value formation procedure, or 
    plausibility note.

    Specific implementations for different message types (e.g., MSCONS) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the STS segment __converter with the syntax parser.

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
    ) -> SegmentSTS:
        """
        Converts STS (Status) segment components to a SegmentSTS object.

        The STS segment is used to specify status information such as correction reason, 
        gas quality, replacement value formation procedure, or plausibility note.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the __converter.

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
