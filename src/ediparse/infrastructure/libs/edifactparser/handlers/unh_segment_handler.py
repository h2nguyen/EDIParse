# coding: utf-8

import logging
from typing import Optional

from . import SegmentHandler
from ..converters import UNHSegmentConverter
from ..exceptions import EdifactParserException
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup, EdifactMessageType
from ..mods.aperak.segments import EdifactAperakMessage
from ..wrappers.segments.message import SegmentUNH
from ..mods.mscons.segments import EdifactMSconsMessage

logger = logging.getLogger(__name__)


class UNHSegmentHandler(SegmentHandler[SegmentUNH]):
    """
    Handler for UNH (Message Header) segments.

    This handler processes UNH segments, which are used to head, identify, and specify 
    a message. It updates the parsing context with the converted UNH segment information, 
    creating a new message and resetting the context for processing a new message.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the UNH segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(UNHSegmentConverter(syntax_parser=syntax_parser))

    def _can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.
        UNH segments can always be handled if the interchange exists.

        Args:
            context: The parsing context to check.

        Returns:
            True if the context is valid, False otherwise.
        """
        return context.interchange is not None

    def _update_context(self, segment: SegmentUNH, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted UNH segment.
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
            elif EdifactMessageType.MSCONS == message_type:
                context.current_message = EdifactMSconsMessage()
            else:
                # TODO, do we still want to continue to parse not registered message types?
                logger.warning(f"Unknown message type: {segment.nachrichten_kennung}.")
                logger.warning(f"Fallback to message type: '{EdifactMessageType.MSCONS}'.")
                context.current_message = EdifactMSconsMessage()
                context.message_type = EdifactMessageType.MSCONS
        context.current_message.unh_nachrichtenkopfsegment = segment
        context.interchange.unh_unt_nachrichten.append(context.current_message)
