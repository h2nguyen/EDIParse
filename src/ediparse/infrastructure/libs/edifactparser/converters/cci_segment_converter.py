# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import (
    SegmentCCI, Merkmalsbeschreibung
)


class CCISegmentConverter(SegmentConverter[SegmentCCI]):
    """
    Converter for CCI (Characteristic/Class ID) segments.

    This converter transforms CCI segment data from EDIFACT format into a structured
    SegmentCCI object. The CCI segment is used to specify product characteristics 
    and the data that defines those characteristics.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the CCI segment converter with the syntax parser.

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
    ) -> SegmentCCI:
        """
        Converts CCI (Characteristic/Class ID) segment components to a SegmentCCI object.

        The CCI segment is used to specify product characteristics and the data that defines those characteristics.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentCCI object with class type code and characteristic description

        Example:
        CCI+15++BI1'
        """
        klassentyp_code = element_components[1]
        gemessene_dimension_code = element_components[2] if len(element_components) > 2 and element_components[
            2] != "" else None
        merkmal_code = element_components[3] if len(element_components) > 3 else None

        return SegmentCCI(
            klassentyp_code=klassentyp_code,
            merkmalsbeschreibung=Merkmalsbeschreibung(
                merkmal_code=merkmal_code
            ) if merkmal_code else None
        )
