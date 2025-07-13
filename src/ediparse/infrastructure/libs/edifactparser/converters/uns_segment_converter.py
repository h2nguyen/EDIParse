# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentUNS


class UNSSegmentConverter(SegmentConverter[SegmentUNS]):
    """
    Converter for UNS (Section Control) segments.

    This __converter transforms UNS segment data from EDIFACT format into a structured
    SegmentUNS object. The UNS segment is used to separate the header and detail 
    sections of a message.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the UNS segment __converter with the syntax parser.

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
    ) -> SegmentUNS:
        """
        Converts UNS (Section Control) segment components to a SegmentUNS object.

        The UNS segment is used to separate the header and detail sections of a message.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the __converter.

        Returns:
            SegmentUNS object with section identification code

        Examples:
        UNS+D'
        """
        abschnittskennung_codiert = element_components[1]
        return SegmentUNS(
            abschnittskennung_codiert=abschnittskennung_codiert
        )
