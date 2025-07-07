# coding: utf-8
"""
Context for parsing EDIFACT-MSCONS messages.

This module provides the context objects used during the parsing of MSCONS messages.
It maintains the state of the current interchange, message, and segment groups
being processed, allowing the parser to build the message structure incrementally.
"""
from typing import Optional

from .segments import (
    EdifactMSconsMessage,
    SegmentGroup1 as MscSG1,
    SegmentGroup2 as MscSG2,
    SegmentGroup4 as MscSG4,
    SegmentGroup5 as MscSG5,
    SegmentGroup6 as MscSG6,
    SegmentGroup7 as MscSG7,
    SegmentGroup8 as MscSG8,
    SegmentGroup9 as MscSG9,
    SegmentGroup10 as MscSG10,
)
from ...wrappers.context import ParsingContext
from ..module_constants import EdifactMessageType


class MSCONSParsingContext(ParsingContext):
    """
    The context that yields all relevant intermittent states during the parsing process of MSCONS messages.

    This class maintains references to the current interchange, message, and segment groups
    being processed during the parsing of an MSCONS message. It allows the parser to
    build the message structure incrementally as segments are encountered in the input.

    According to the MSCONS D.04B 2.4c standard, messages have a hierarchical structure
    with segment groups that can be nested. This context helps track the current position
    in this hierarchy during parsing.
    """

    current_sg1: Optional[MscSG1] = None
    current_sg2: Optional[MscSG2] = None
    current_sg4: Optional[MscSG4] = None
    current_sg5: Optional[MscSG5] = None
    current_sg6: Optional[MscSG6] = None
    current_sg7: Optional[MscSG7] = None
    current_sg8: Optional[MscSG8] = None
    current_sg9: Optional[MscSG9] = None
    current_sg10: Optional[MscSG10] = None

    def __init__(self, **kwargs):
        """
        Initialize a new MSCONS parsing context.

        Initializes the message type and empty the current message.
        """
        kwargs.setdefault("message_type", EdifactMessageType.MSCONS)
        kwargs.setdefault("current_message", EdifactMSconsMessage())
        super().__init__(**kwargs)

    def reset_for_new_message(self) -> None:
        """
        Reset the context for a new message.

        This method is called when a new message is started (typically when a UNH segment
        is encountered). It resets all current segment group references to None.

        According to the MSCONS D.04B 2.4c standard, each message starts with a UNH segment
        and has its own hierarchy of segment groups, so the context needs to be reset
        for each new message.
        """
        self.current_message = EdifactMSconsMessage()
        self.current_sg1 = None
        self.current_sg2 = None
        self.current_sg4 = None
        self.current_sg5 = None
        self.current_sg6 = None
        self.current_sg7 = None
        self.current_sg8 = None
        self.current_sg9 = None
        self.current_sg10 = None
