# coding: utf-8

from typing import Optional

from ....handlers.com_segment_handler import COMSegmentHandler
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentCOM


class APERAKCOMSegmentHandler(COMSegmentHandler):
    """
    APERAK-specific handler for COM (Communication Contact) segments.

    This handler processes COM segments in APERAK messages, which provide communication information 
    such as telephone numbers, email addresses, etc. It updates the parsing context
    with the converted COM segment information, appending it to the appropriate segment group.

    In APERAK messages, COM segments are used in segment group SG3.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the APERAK COM segment handler with the appropriate __converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser)

    def _update_context(self, segment: SegmentCOM, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted COM segment for APERAK messages.
        The update depends on the current segment group.

        Args:
            segment: The converted COM segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG3 == current_segment_group:
            context.current_sg3.com_kommunikationsverbindungen.append(segment)