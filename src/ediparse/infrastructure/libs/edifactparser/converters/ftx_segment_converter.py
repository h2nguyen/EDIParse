# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentFTX, Text


class FTXSegmentConverter(SegmentConverter[SegmentFTX]):
    """
    Converter for FTX (Free Text) segments in EDIFACT APERAK messages.

    The FTX segment is used to provide textual information in free format.
    In APERAK messages, it is commonly used to provide detailed descriptions
    of errors or to give additional information about the acknowledgement.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the FTX segment __converter with the syntax parser.

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
    ) -> SegmentFTX:
        """
        Converts FTX (Free Text) segment components to a SegmentFTX object.

        The FTX segment provides textual information in free format, commonly used
        for detailed descriptions of errors or additional information.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the __converter.

        Returns:
            SegmentFTX object with text details

        Examples:
        FTX+Z02+++Referenz Vorgangsnummer (aus Anfragenachricht):RFF?+TN?:TG9523'
        FTX+ABO+++201609160400201609090400?:719'
        """
        text_details = self._syntax_parser.split_components(
            string_content=element_components[4],
            context=context,
            include_escape_symbol=False
        )

        return SegmentFTX(
            textbezug_qualifier=element_components[1],
            text=Text(
                freier_text_m=text_details[0],
                freier_text_c=text_details[1] if len(text_details) > 1 else None,
            ),
        )