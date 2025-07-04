# coding: utf-8
"""
Context for parsing EDIFACT messages.

This module provides the context objects used during the parsing of EDIFACT messages.
It maintains the state of the current interchange, message, and segment groups
being processed, allowing the parser to build the message structure incrementally.
"""

from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel

from .constants import EdifactMessageType
from .segments.base import AbstractEdifactMessage
from .segments.message_structure import EdifactInterchange


class ParsingContext(BaseModel, ABC):
    """
    The interface for context objects that yield all relevant intermittent states during the parsing process.

    This interface defines the common properties and methods for context objects used in parsing
    different types of EDIFACT messages. It allows the parser to build the message structure 
    incrementally as segments are encountered in the input.

    EDIFACT messages have a hierarchical structure with segment groups that can be nested.
    This context helps track the current position in this hierarchy during parsing.
    """

    segment_count: int = 0
    interchange: EdifactInterchange = EdifactInterchange()
    current_message: Optional[AbstractEdifactMessage] = None
    message_type: Optional[EdifactMessageType] = None

    @abstractmethod
    def reset_for_new_message(self) -> None:
        """
        Reset the context for a new message.

        This method is called when a new message is started (typically when a UNH segment
        is encountered). It resets all current segment group references to None.

        Each EDIFACT message starts with a UNH segment and has its own hierarchy of 
        segment groups, so the context needs to be reset for each new message.
        """
        pass


class InitialParsingContext(ParsingContext):
    """
    A context class used for the initial parsing process.

    This class is used at the beginning of the parsing process when there is no specific
    content for the context yet. The context will be later updated based on the message
    type provided within the EDIFACT input information.
    """
    pass

    def reset_for_new_message(self) -> None:
        pass
