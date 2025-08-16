# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..exceptions import CONTRLException
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentUNA


class UNASegmentConverter(SegmentConverter[SegmentUNA]):
    """
    Converter for UNA (Service String Advice) segments.

    The UNA segment is always exactly 9 characters long and defines the special characters
    used as delimiters in the EDIFACT message.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the UNA segment __converter with the syntax parser.

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
    ) -> SegmentUNA:
        """
        Converts UNA (Service String Advice) segment to a SegmentUNA object.

        The UNA segment is special as it doesn't follow the normal EDIFACT segment structure.
        It's always exactly 9 characters long and each position has a specific meaning.

        Args:
            element_components: List of segment components (should be a single string "UNA:+.? '")
            last_segment_type: The type of the previous segment (should be None as UNA is typically the first segment)
            current_segment_group: The current segment group being processed (should be None)
            context: The context to use for the __converter.

        Returns:
            SegmentUNA object with the delimiter characters defined in the UNA segment

        Example:
            UNA:+.? '
        """
        # The UNA segment should be a single string like: UNA:+.? '
        una_segment = element_components[0]

        # Ensure the segment is a valid UNA segment
        if not una_segment.startswith("UNA") or len(una_segment) != 9:
            error_message = f"Invalid UNA segment: {una_segment}. UNA segment must be exactly 9 characters long."
            raise CONTRLException(message=error_message)

        # Extract the delimiter characters
        component_separator = una_segment[3]
        element_separator = una_segment[4]
        decimal_mark = una_segment[5]
        release_character = una_segment[6]
        reserved = una_segment[7]
        segment_terminator = una_segment[8]

        return SegmentUNA(
            component_separator=component_separator,
            element_separator=element_separator,
            decimal_mark=decimal_mark,
            release_character=release_character,
            reserved=reserved,
            segment_terminator=segment_terminator
        )
