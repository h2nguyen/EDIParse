# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentERC, Anwendungsfehler


class ERCSegmentConverter(SegmentConverter[SegmentERC]):
    """
    Converter for ERC (Application Error Detail) segments in EDIFACT APERAK messages.

    The ERC segment is used to identify the type of application error that has occurred
    during the processing of a message. It contains error codes that indicate specific
    issues encountered.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the ERC segment converter with the syntax parser.

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
    ) -> SegmentERC:
        """
        Converts ERC (Application Error Detail) segment components to a SegmentERC object.

        The ERC segment contains error codes that indicate specific issues encountered
        during message processing.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentERC object with error code details

        Examples:
        ERC+Z10'
        """
        return SegmentERC(
            fehlercode=Anwendungsfehler(anwendungsfehler_code=element_components[1])
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        pass
