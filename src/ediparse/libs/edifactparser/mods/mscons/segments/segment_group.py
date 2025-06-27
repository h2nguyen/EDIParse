# coding: utf-8
"""
Models for segment groups in the MSCONS message.

This module consolidates all segment groups defined in the MSCONS D.04B 2.4c standard.
According to the standard, segment groups form a hierarchical structure that organizes
the segments in a message.
"""

from typing import Optional

from pydantic import BaseModel, Field

from ....wrappers.segments.partner import SegmentNAD, SegmentCTA, SegmentCOM
from ....wrappers.segments.reference import SegmentDTM, SegmentRFF
from ....wrappers.segments import (
    SegmentLOC, SegmentCCI, SegmentLIN, SegmentPIA, SegmentQTY, SegmentSTS
)


class SegmentGroup1(BaseModel):
    """
    SG1 (C 9) - Reference group (Referenzgruppe)

    Contains reference information and associated date/time data.

    According to MSCONS D.04B 2.4c, this segment group includes:
    - RFF: Reference (M 1) - Mandatory reference information
    - DTM: Date/Time/Period (M 9) - Mandatory date/time information, can occur up to 9 times

    This group is used for various references such as:
    - Process ID (Prüfidentifikator)
    - Reference to previous master data notification from the MSB
    - Version information for market location-specific allocation list for gas (MMMA)
    """
    rff_referenzangaben: Optional[SegmentRFF] = None  # M 1
    dtm_versionsangabe_marktlokationsscharfe_allokationsliste_gas_mmma: list[SegmentDTM] = Field(
        default_factory=list)  # M 9


class SegmentGroup4(BaseModel):
    """
    SG4 (C 9 in SG2) - Contact information group (Kontaktinformationsgruppe)

    Contains contact information for a market partner.

    According to MSCONS D.04B 2.4c, this segment group includes:
    - CTA: Contact information (M 1) - Mandatory contact function information
    - COM: Communication contact (C 9) - Optional communication information, can occur up to 9 times

    This group is used to provide contact details for the market partners identified in SG2.
    """
    cta_ansprechpartner: Optional[SegmentCTA] = None
    com_kommunikationsverbindung: list[SegmentCOM] = Field(default_factory=list)


class SegmentGroup2(BaseModel):
    """
    SG2 (C 99) - Market partner group (Marktpartnergruppe)

    Identifies market partners involved in the message.

    According to MSCONS D.04B 2.4c, this segment group includes:
    - NAD: Name and address (M 1) - Mandatory party identification
    - SG4: Contact information (C 9) - Optional contact information, can occur up to 9 times

    This group is used to identify the sender (MS), recipient (MR), and other parties
    involved in the message, along with their contact information.
    """
    nad_marktpartner: Optional[SegmentNAD] = None  # M 1
    sg4_kontaktinformationen: list[SegmentGroup4] = Field(default_factory=list)


class SegmentGroup10(BaseModel):
    """
    SG10 (M 9999) in SG9 - Quantity and status information group
    (Mengen- und Statusangabengruppe)

    Contains quantity values, their timestamps, and status information.

    According to MSCONS D.04B 2.4c, this segment group includes:
    - QTY: Quantity (M 1) - Mandatory quantity information
    - DTM: Date/Time/Period (C 9) - Optional time information, can occur up to 9 times
    - STS: Status (C 9) - Optional status information, can occur up to 9 times

    This group is used to provide the actual measurement values along with their
    timestamps and status information.
    """
    qty_mengenangaben: Optional[SegmentQTY] = None  # Quantity information
    dtm_zeitangaben: list[SegmentDTM] = Field(default_factory=list)  # Time information
    sts_statusangaben: list[SegmentSTS] = Field(default_factory=list)  # Status information


class SegmentGroup9(BaseModel):
    """
    SG9 (C 99999) in SG6 - Position data group (Positionsdatengruppe)

    Contains line items with their product identification and quantity/status information.

    According to MSCONS D.04B 2.4c, this segment group includes:
    - LIN: Line item (M 1) - Mandatory line item information
    - PIA: Additional product ID (C 9) - Optional product identification, can occur up to 9 times
    - SG10: Quantity and status information (M 9999) - Mandatory quantity information,
      can occur up to 9999 times

    This group is used to provide detailed measurement data for specific line items.
    """
    lin_lfd_position: Optional[SegmentLIN] = None  # Line item information
    pia_produktidentifikation: Optional[SegmentPIA] = None  # Product identification
    sg10_mengen_und_statusangaben: list[SegmentGroup10] = Field(default_factory=list)  # Quantity and status information


class SegmentGroup8(BaseModel):
    """
    SG8 (C 99) in SG6 - Time series type group (Zeitreihentypengruppe)

    Identifies the type of time series.

    According to MSCONS D.04B 2.4c, this segment group includes:
    - CCI: Composite Code Information (M 1) - Mandatory time series type information

    This group is used to specify the type of time series being reported.
    """
    cci_zeitreihentyp: Optional[SegmentCCI] = None  # Time series type


class SegmentGroup7(BaseModel):
    """
    SG7 (C 99) in SG6 - Reference information group (Referenzangabengruppe)

    Contains reference information related to the location.

    According to MSCONS D.04B 2.4c, this segment group includes:
    - RFF: Reference (M 1) - Mandatory reference information

    This group is used for references such as:
    - Device number (Gerätenummer)
    - Configuration ID (Konfigurations-ID)
    """
    rff_referenzangabe: Optional[SegmentRFF] = None  # e.g., device number, configuration ID


class SegmentGroup6(BaseModel):
    """
    SG6 (M 99999) in SG5 - Value and recording information for the object
    (Wert- und Erfassungsangaben zum Objekt)

    Contains detailed information about an object, including its identification,
    time periods, references, time series types, and position data.

    According to MSCONS D.04B 2.4c, this segment group includes:
    - LOC: Place/Location Identification (M 1) - Mandatory location information
    - DTM: Date/Time/Period (C 9) - Optional time period information, can occur up to 9 times
    - SG7: Reference information (C 99) - Optional reference information, can occur up to 99 times
    - SG8: Time series type (C 99) - Optional time series type information, can occur up to 99 times
    - SG9: Position data (C 99999) - Optional position data, can occur up to 99999 times

    This group is used to provide detailed information about objects such as metering points.
    """
    loc_identifikationsangabe: Optional[SegmentLOC] = None
    dtm_zeitraeume: list[SegmentDTM] = Field(default_factory=list)
    sg7_referenzangaben: list[SegmentGroup7] = Field(default_factory=list)
    sg8_zeitreihentypen: list[SegmentGroup8] = Field(default_factory=list)
    sg9_positionsdaten: list[SegmentGroup9] = Field(default_factory=list)


class SegmentGroup5(BaseModel):
    """
    SG5 (M 99999) - Delivery or supply location group (Liefer- bzw. Bezugsortsgruppe)

    Identifies a delivery or supply location and contains detailed information about it.

    According to MSCONS D.04B 2.4c, this segment group includes:
    - NAD: Name and Address (M 1) - Mandatory location identification
    - SG6: Value and recording information for the object (M 99999) - Mandatory object information,
      can occur up to 99999 times

    This group is used to identify delivery locations and provide detailed information about them.
    """
    nad_name_und_adresse: Optional[SegmentNAD] = None
    sg6_wert_und_erfassungsangaben_zum_objekt: list[SegmentGroup6] = Field(default_factory=list)
