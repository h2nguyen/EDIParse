# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..utils import EdifactSyntaxHelper
from ..wrappers.constants import SegmentGroup
from ..wrappers.context import ParsingContext
from ..wrappers.segments import SegmentBGM


class BGMSegmentHandler(SegmentHandler[SegmentBGM]):
    """
    Handler for BGM (Beginning of Message) segments.

    This handler processes BGM segments, which identify the type and function of a message
    and transmit its identifying number. It updates the parsing context with the converted
    BGM segment information.

    Currently, this handler supports both MSCONS and APERAK messages, where BGM segments
    are used in the header of the message to identify the message type and function.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the BGM segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(
            syntax_helper=syntax_helper,
        )

    def _update_context(self, segment: SegmentBGM, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted BGM segment.

        Args:
            segment: The converted BGM segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.current_message.bgm_beginn_der_nachricht = segment
