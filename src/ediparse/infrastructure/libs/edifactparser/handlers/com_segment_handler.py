# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..converters import COMSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup, EdifactMessageType
from ..wrappers.segments import SegmentCOM


class COMSegmentHandler(SegmentHandler[SegmentCOM]):
    """
    Handler for COM (Communication Contact) segments.

    This handler processes COM segments, which provide communication information 
    such as telephone numbers, email addresses, etc. It updates the parsing context
    with the converted COM segment information, appending it to the appropriate segment group.

    Currently, this handler supports both MSCONS and APERAK messages:
    - In MSCONS messages, COM segments are used in segment group SG4
    - In APERAK messages, COM segments are used in segment group SG3
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the COM segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(COMSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentCOM, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted COM segment.
        The update depends on the current segment group.

        Args:
            segment: The converted COM segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if EdifactMessageType.MSCONS == context.message_type:
            if SegmentGroup.SG4 == current_segment_group:
                context.current_sg4.com_kommunikationsverbindung.append(segment)

        if EdifactMessageType.APERAK == context.message_type:
            if SegmentGroup.SG3 == current_segment_group:
                context.current_sg3.com_kommunikationsverbindungen.append(segment)
