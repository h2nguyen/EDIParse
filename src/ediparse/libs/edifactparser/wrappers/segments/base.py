# coding: utf-8
"""
Base classes for EDIFACT message structures.

This module defines the abstract base class that all EDIFACT message types
should inherit from, establishing a common interface and structure.
"""

from abc import ABC
from typing import Optional

from pydantic import BaseModel, Field

from ...wrappers.segments.message import SegmentUNH, SegmentBGM, SegmentUNT
from ...wrappers.segments.reference import SegmentDTM


class AbstractEdifactMessage(BaseModel, ABC):
    """
    Abstract base class for all EDIFACT message types.

    This class defines the common structure that all EDIFACT messages should follow.
    Specific message types (MSCONS, APERAK, etc.) should inherit from this class
    and implement their specific fields and behavior.

    Design Pattern:
    --------------
    This class implements a combination of:
    1. Inheritance pattern: Using an abstract base class (ABC) to define a common interface
       that all EDIFACT message types must implement.
    2. Composition pattern: Message types are composed of various segments and segment groups.

    Discriminated Unions:
    -------------------
    The derived classes use Pydantic v2's Discriminated Unions feature through the 'message_type' 
    field which acts as a discriminator. This allows for:
    - Proper type checking during deserialization
    - Correct JSON serialization of different message types
    - Runtime type identification

    When used with EdifactMessageUnion (defined in message_structure.py), the system can 
    automatically determine the correct message type based on the 'message_type' field value.

    Example:
    -------
    ```python
    EdifactMessageUnion = Annotated[
        Union[
            EdifactAperakMessage,
            EdifactMSconsMessage,
        ],
        Field(discriminator="message_type")
    ]
    ```

    This design improves code flexibility by allowing:
    - Easy addition of new message types without changing existing code
    - Polymorphic handling of different message types
    - Type-safe operations on message collections
    """
    # These fields are defined generically without specific segment type dependencies
    # Concrete implementations will override these with their specific segment types
    unh_nachrichtenkopfsegment: Optional[SegmentUNH] = Field(default=None)  # Message header
    bgm_beginn_der_nachricht: Optional[SegmentBGM] = Field(default=None)  # Beginning of a message
    dtm_nachrichtendatum: list[SegmentDTM] = Field(default_factory=list)  # Message date
    unt_nachrichtenendsegment: Optional[SegmentUNT] = Field(default=None)  # Message trailer
