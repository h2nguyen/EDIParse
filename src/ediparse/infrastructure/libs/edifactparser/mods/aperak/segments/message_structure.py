"""
Models for the complete APERAK message structure.

These models represent the overall structure of APERAK messages and interchanges.
APERAK (Application error and acknowledgement message) is used to inform a message issuer
that their message has been received by the recipient's application and has been processed
with or without errors.
"""
from typing import Optional, Literal
from pydantic import Field

from .segment_group import SegmentGroup2, SegmentGroup3, SegmentGroup4
from ....wrappers.constants import EdifactMessageType
from ....wrappers.segments import SegmentUNT
from ....wrappers.segments.base import AbstractEdifactMessage


class EdifactAperakMessage(AbstractEdifactMessage):
    """
    Represents an APERAK message within an interchange.

    An APERAK message contains information about the acknowledgement status of a previously
    received message, including any errors encountered during processing.

    Implementation Notes:
    -------------------
    This class inherits from AbstractEdifactMessage and implements the APERAK-specific
    structure. It includes a 'message_type' field set to EdifactMessageType.APERAK,
    which serves as the discriminator for the Discriminated Unions pattern.

    The 'message_type' field is marked with exclude=True to prevent it from being included
    in serialization directly, as it's only used for type discrimination.

    See AbstractEdifactMessage for more details on the design pattern and Discriminated Unions.
    """
    message_type: Literal[EdifactMessageType.APERAK] = Field(
        default=EdifactMessageType.APERAK,
        exclude=True
    )

    # APERAK-specific fields
    sg2_referenzen: list[SegmentGroup2] = Field(default_factory=list)  # References
    sg3_marktpartnern: list[SegmentGroup3] = Field(default_factory=list)  # Market partners
    sg4_fehler_beschreibung: list[SegmentGroup4] = Field(default_factory=list)  # Error description
    unt_nachrichtenendsegment: Optional[SegmentUNT] = Field(default=None)  # Message trailer
