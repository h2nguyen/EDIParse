# coding: utf-8
"""
Models related to locations in EDIFACT messages (NAD, LOC).

These models represent location information and related data in EDIFACT messages.
These segments are used to identify delivery locations, balance groups, and objects, 
along with their associated data, primarily in MSCONS message types.
"""

from typing import Optional

from pydantic import BaseModel


class Ortsangabe(BaseModel):
    """
    Location information (Ortsangabe).

    Contains the location code, such as a balance group identifier.

    In EDIFACT messages, this includes:
    - Location identification code (e.g., balance group ID)
    """
    ortsangabe_code: Optional[str] = None  # Bilanzkreis an, e.g., '51078306269'


class ZugehoerigerOrt1Identifikation(BaseModel):
    """
    Associated location 1, identification (Zugehöriger Ort 1, Identifikation).

    Contains the associated location code, such as a related balance group identifier.

    In EDIFACT messages, this includes:
    - First related location identification code (e.g., balance group ID)
    """
    erster_zugehoeriger_platz_ort_code: Optional[str] = None  # Bilanzkreis von, e.g., '51078306269'


class SegmentLOC(BaseModel):
    """
    LOC-Segment (Place/Location Identification / Standort-/Ortskennung)

    Identifies a location or place relevant to the message.

    This segment is primarily used in MSCONS message types and includes:
    - Location qualifier (identifies the type of location)
    - Location identification (identifies the specific location)
    - Associated location 1 (identifies a related location)

    Common qualifiers include:
    - '16': Balance group (Bilanzkreis)
    - '17': Object (Objekt)
    - '237': Balance group (Bilanzkreis)
    """
    ortsangabe_qualifier: Optional[str] = None  # e.g., '237' Bilanzkreis
    ortsangabe: Optional[Ortsangabe] = None
    zugehoeriger_ort_1_identifikation: Optional[ZugehoerigerOrt1Identifikation] = None


class EinzelheitenZuMassangaben(BaseModel):
    """
    Details on measurement specifications (Einzelheiten zu Maßangaben).

    Contains information about the measured dimension.

    In EDIFACT messages, this includes:
    - Measured attribute code (identifies the type of measurement)
    """
    gemessene_dimension_code: Optional[str] = None  # Code for the measured dimension


class Merkmalsbeschreibung(BaseModel):
    """
    Characteristic description (Merkmalsbeschreibung).

    Contains information about the characteristic being described.

    In EDIFACT messages, this includes:
    - Characteristic code (identifies the specific characteristic)
    """
    merkmal_code: Optional[str] = None  # Code for the characteristic


class SegmentCCI(BaseModel):
    """
    CCI-Segment (Composite Code Information / Kennzeichnung des Zeitreihentyps)

    Identifies the type of time series or characteristic.

    This segment is primarily used in MSCONS message types and includes:
    - Class type code (identifies the type of class)
    - Characteristic description (identifies the specific characteristic)
    """
    klassentyp_code: Optional[str] = None  # Type of class
    merkmalsbeschreibung: Optional[Merkmalsbeschreibung] = None  # Specific characteristic
