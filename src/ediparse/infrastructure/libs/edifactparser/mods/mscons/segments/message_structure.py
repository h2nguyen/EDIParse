# coding: utf-8
"""
Models for the MSCONS message structure.

This model represents the overall structure of MSCONS messages.
According to the MSCONS D.04B 2.4c standard, a message follows a specific structure with segment groups.
"""

from typing import Optional, List, Literal
from pydantic import Field

from .segment_group import (
    SegmentGroup1, SegmentGroup2, SegmentGroup5
)
from ...module_constants import EdifactMessageType
from ....wrappers.segments.base import AbstractEdifactMessage
from ....wrappers.segments import SegmentUNS


class EdifactMSconsMessage(AbstractEdifactMessage):
    """
    Represents an EDIFACT-MSCONS message (UNH...UNT).

    According to MSCONS D.04B 2.4c, a message consists of:
    1. A header section with:
       - UNH: Message header (M 1)
       - BGM: Beginning of message (M 1)
       - DTM: Date/time/period (M 9)
       - SG1: Reference (C 9)
       - SG2: Market partner (C 99)
    2. A section control segment (UNS) separating header and detail
    3. A detail section with:
       - SG5: Delivery/supply location (M 99999)
    4. A message trailer (UNT)

    This structure follows the branching diagram in the MSCONS documentation,
    which shows the hierarchical relationship between segments and segment groups.

    Implementation Notes:
    -------------------
    This class inherits from AbstractEdifactMessage and implements the MSCONS-specific
    structure. It includes a 'message_type' field set to EdifactMessageType.MSCONS,
    which serves as the discriminator for the Discriminated Unions pattern.

    The 'message_type' field is marked with exclude=True to prevent it from being included
    in serialization directly, as it's only used for type discrimination.

    See AbstractEdifactMessage for more details on the design pattern and Discriminated Unions.
    """
    message_type: Literal[EdifactMessageType.MSCONS] = Field(
        default=EdifactMessageType.MSCONS,
        exclude=True
    )

    # MSCONS-specific fields
    sg1_referenzen: List[SegmentGroup1] = Field(default_factory=list)  # References
    sg2_marktpartnern: List[SegmentGroup2] = Field(default_factory=list)  # Market partners
    uns_abschnitts_kontrollsegment: Optional[SegmentUNS] = Field(default=None)  # Section control
    sg5_liefer_bzw_bezugsorte: List[SegmentGroup5] = Field(default_factory=list)  # Delivery locations
