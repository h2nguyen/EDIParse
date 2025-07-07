# coding: utf-8

import logging
from typing import Optional

from ....handlers.unh_segment_handler import UNHSegmentHandler
from ....exceptions import EdifactParserException
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup, EdifactMessageType
from ....wrappers.segments.message import SegmentUNH
from ..segments import EdifactAperakMessage

logger = logging.getLogger(__name__)


class APERAKUNHSegmentHandler(UNHSegmentHandler):
    """
    APERAK-specific handler for UNH (Message Header) segments.

    This handler processes UNH segments in APERAK messages, which are used to head, identify, 
    and specify a message. It updates the parsing context with the converted UNH segment 
    information, creating a new APERAK message and resetting the context for processing a new message.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the APERAK UNH segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser)

    def _update_context(self, segment: SegmentUNH, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted UNH segment for APERAK messages.
        This also resets the context for a new message.

        Args:
            segment: The converted UNH segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        # Reset for a new message
        context.reset_for_new_message()

        if segment.nachrichten_kennung is None:
            raise EdifactParserException("nachrichten_kennung should not be None.")
        else:
            message_type = segment.nachrichten_kennung.nachrichtentyp_kennung.upper()
            if EdifactMessageType.APERAK == message_type:
                context.current_message = EdifactAperakMessage()
                context.message_type = EdifactMessageType.APERAK
            else:
                # If the message type is not APERAK, we still create an APERAK message as a fallback
                logger.warning(f"Expected APERAK message type, but got: {segment.nachrichten_kennung}.")
                logger.warning(f"Fallback to message type: '{EdifactMessageType.APERAK}'.")
                context.current_message = EdifactAperakMessage()
                context.message_type = EdifactMessageType.APERAK

        context.current_message.unh_nachrichtenkopfsegment = segment
        context.interchange.unh_unt_nachrichten.append(context.current_message)