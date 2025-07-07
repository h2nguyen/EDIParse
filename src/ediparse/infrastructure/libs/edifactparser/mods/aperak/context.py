"""
Context for parsing EDIFACT-APERAK messages.

This module provides the context object used during the parsing of APERAK messages.
It maintains the state of the current interchange, message, and segment groups
being processed, allowing the parser to build the message structure incrementally.
"""
from typing import Optional

from .segments import (
    EdifactAperakMessage, SegmentGroup2, SegmentGroup3, SegmentGroup4, SegmentGroup5
)
from ...wrappers.context import ParsingContext
from ..module_constants import EdifactMessageType


class APERAKParsingContext(ParsingContext):
    """
    The context that yields all relevant intermittent states during the parsing process of APERAK messages.

    This class maintains references to the current interchange, message, and segment groups
    being processed during the parsing of an APERAK message. It allows the parser to
    build the message structure incrementally as segments are encountered in the input.

    APERAK (Application Error and Acknowledgement Message, version UN D.07B S3 2.1i standard) is used to
    inform a message issuer that their message has been received by the recipient's application. Furthermore,
    it indicates whether the message has been accepted or rejected due to errors encountered during processing.
    """

    current_sg2: Optional[SegmentGroup2] = None
    current_sg3: Optional[SegmentGroup3] = None
    current_sg4: Optional[SegmentGroup4] = None
    current_sg5: Optional[SegmentGroup5] = None

    def __init__(self, **kwargs):
        """
        Initialize a new APERAK parsing context.

        Initializes the message type and empty the current message.
        """
        kwargs.setdefault("message_type", EdifactMessageType.APERAK)
        kwargs.setdefault("current_message", EdifactAperakMessage())
        super().__init__(**kwargs)

    def reset_for_new_message(self) -> None:
        """
        Reset the context for a new message.

        This method is called when a new message is started (typically when a UNH segment
        is encountered). It resets all APERAK-specific states.
        """
        # Reset APERAK-specific state here
        self.current_message = EdifactAperakMessage()
        self.current_sg2 = None
        self.current_sg3 = None
        self.current_sg4 = None
        self.current_sg5 = None
