# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentUNZ


class UNZSegmentConverter(SegmentConverter[SegmentUNZ]):
    """
    Converter for UNZ (Interchange Trailer) segments.

    This converter transforms UNZ segment data from EDIFACT format into a structured
    SegmentUNZ object. The UNZ segment is used to end and check the completeness of an 
    interchange, containing the count of messages in the interchange and the interchange reference.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the UNZ segment converter with the syntax parser.

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
    ) -> SegmentUNZ:
        """
        Converts UNZ (Interchange Trailer) segment components to a SegmentUNZ object.

        The UNZ segment is used to end and check the completeness of an interchange.
        It contains the count of messages in the interchange and the interchange reference.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentUNZ object with message count and interchange reference

        Examples:
        UNZ+1+ABC4711'
        """
        anzahl_msg = int(element_components[1])
        datenaustauschreferenz = element_components[2]
        return SegmentUNZ(
            datenaustauschzaehler=anzahl_msg,
            datenaustauschreferenz=datenaustauschreferenz
        )
