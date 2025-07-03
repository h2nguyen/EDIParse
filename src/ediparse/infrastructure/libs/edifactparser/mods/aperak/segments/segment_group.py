"""
Models for segment groups in the APERAK message.

This module consolidates all segment groups defined in the APERAK message structure.
Segment groups form a hierarchical structure that organizes the segments in a message,
allowing for logical grouping of related information such as references, market partners,
and error descriptions.
"""
from typing import Optional

from pydantic import BaseModel, Field

from ....wrappers.segments.partner import SegmentNAD, SegmentCTA, SegmentCOM
from ....wrappers.segments.reference import SegmentDTM, SegmentRFF
from ....wrappers.segments import SegmentFTX, SegmentERC


class SegmentGroup2(BaseModel):
    """
    Represents a reference information group in an APERAK message.

    This segment group contains reference information (RFF) and associated dates (DTM)
    that identify the message being acknowledged.
    """
    rff_referenzangaben: Optional[SegmentRFF] = None  # M 1
    dtm_referenzdatum: list[SegmentDTM] = Field(
        default_factory=list)  # M 9


class SegmentGroup3(BaseModel):
    """
    Represents a market partner information group in an APERAK message.

    This segment group contains information about a market participant (NAD),
    including contact persons (CTA) and communication details (COM).
    """
    nad_marktpartner: Optional[SegmentNAD] = None  # M 1
    cta_ansprechpartnern: list[SegmentCTA] = Field(default_factory=list)
    com_kommunikationsverbindungen: list[SegmentCOM] = Field(default_factory=list)


class SegmentGroup5(BaseModel):
    """
    Represents a reference text group in an APERAK message.

    This segment group contains reference information (RFF) and associated free text (FTX)
    that provide additional details about a specific reference in the error context.
    """
    rff_referenz: Optional[SegmentRFF] = None
    ftx_referenz_texte: list[SegmentFTX] = Field(default_factory=list)


class SegmentGroup4(BaseModel):
    """
    Represents an error description group in an APERAK message.

    This segment group contains error code information (ERC), explanatory free text (FTX),
    and references to specific parts of the message that contain errors (SG5).
    It is the core part of the APERAK message that communicates error details.
    """
    erc_error_code: Optional[SegmentERC] = None
    ftx_freier_text: Optional[SegmentFTX] = None
    sg5_nachrichtenreferenzen: list[SegmentGroup5] = Field(default_factory=list)
