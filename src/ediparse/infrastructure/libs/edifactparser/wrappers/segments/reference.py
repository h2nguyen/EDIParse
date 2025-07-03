# coding: utf-8
"""
Models related to references in EDIFACT messages (RFF, DTM).

These models represent date/time information and references in EDIFACT messages.
These segments are used to provide additional reference information and date/time 
specifications in both MSCONS and APERAK message types.
"""

from typing import Optional

from pydantic import BaseModel


class SegmentDTM(BaseModel):
    """
    DTM-Segment (Date/Time/Period / Datums-/Zeitangabe)

    Contains date or time information in code form.

    This segment is used in both MSCONS and APERAK message types and can include:
    - Date/time/period qualifier (e.g., '137' for Document/message date/time)
    - Date/time/period value (the actual date/time value)
    - Date/time/period format code (e.g., '303' for CCYYMMDDHHMMZZZ)

    Common qualifiers include:
    - '137': Document/message date/time (Nachrichtendatum/-zeit)
    - '163': Processing period, start date/time (Verarbeitung, Beginndatum/-zeit)
    - '164': Processing period, end date/time (Verarbeitung, Endedatum/-zeit)
    """
    bezeichner: Optional[str] = None  # NON-EDIFACT custom technical field
    datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier: Optional[
        str] = None  # e.g., '137' Dokumenten-/Nachrichtendatum/-zeit
    datum_oder_uhrzeit_oder_zeitspanne_wert: Optional[str] = None  # e.g., '202308150730000'
    datums_oder_uhrzeit_oder_zeitspannen_format_code: Optional[str] = None  # e.g., '303' (Format CCYYMMDDHHMMZZZ)


class SegmentRFF(BaseModel):
    """
    RFF-Segment (Reference / Referenzangabe)

    References another identifier (e.g., order number, process ID).

    This segment is used in both MSCONS and APERAK message types and includes:
    - Reference qualifier (identifies the type of reference)
    - Reference number (the actual reference value)

    Common qualifiers include:
    - 'Z13': Process ID (Prüfidentifikator)
    - 'AGI': Application number (Beantragungsnummer)
    - 'ACW': Previous message (Vorangegangene Nachricht)
    - '23': Device number (Gerätenummer)
    - '24': Configuration ID (Konfigurations-ID)
    """
    bezeichner: Optional[str] = None  # NON-EDIFACT custom technical field
    referenz_qualifier: Optional[str] = None  # e.g., 'Z13' Prüfidentifikator
    referenz_identifikation: Optional[str] = None  # e.g., '13025'
