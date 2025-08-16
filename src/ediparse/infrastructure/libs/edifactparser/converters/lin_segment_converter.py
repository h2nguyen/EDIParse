# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentLIN


class LINSegmentConverter(SegmentConverter[SegmentLIN]):
    """
    Converter for LIN (Line Item) segments.

    This __converter transforms LIN segment data from EDIFACT format into a structured
    SegmentLIN object. The LIN segment identifies a line item and its configuration 
    in a message.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the LIN segment __converter with the syntax parser.

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
    ) -> SegmentLIN:
        """
        Converts LIN (Line Item) segment components to a SegmentLIN object.

        The LIN segment identifies a line item and its configuration in a message.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the __converter.

        Returns:
            SegmentLIN object with position number

        Example:
        LIN+1'
        """
        return SegmentLIN(
            positionsnummer=element_components[1]
        )
