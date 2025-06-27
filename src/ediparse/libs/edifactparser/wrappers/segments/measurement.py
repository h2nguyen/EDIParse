# coding: utf-8
"""
Models related to measurements in EDIFACT messages (LIN, PIA, QTY, STS).

These models represent measurement data and related information in EDIFACT messages.
These segments are used to provide detailed measurement values, their units, 
status information, and timestamps, primarily in MSCONS message types.
"""

from typing import Optional

from pydantic import BaseModel


class SegmentLIN(BaseModel):
    """
    LIN-Segment (Line Item / Zeilenelement)

    Identifies a line item within a position group, often used with OBIS codes.

    This segment is primarily used in MSCONS message types and includes:
    - Line item number (sequential position number)

    This segment is used to provide a sequential numbering of line items.
    """
    positionsnummer: Optional[str] = None  # lfd. Position


class WarenLeistungsnummerIdentifikation(BaseModel):
    """
    Product/service number identification (Waren-/Leistungsnummer, Identifikation).

    Contains the product/service number and its type.

    In EDIFACT messages, this includes:
    - Product/service ID number (the actual identifier)
    - Code list qualifier (identifies the type of product/service number)
    """
    produkt_leistungsnummer: Optional[str] = None  # The actual product/service number
    art_der_produkt_leistungsnummer_code: Optional[str] = None  # Type of product/service number


class SegmentPIA(BaseModel):
    """
    PIA-Segment (Additional Product ID / Zusatzproduktkennung)

    Provides additional product identification information.

    This segment is primarily used in MSCONS message types and includes:
    - Product ID function qualifier (identifies the function of the product ID)
    - Product/service ID (identifies the specific product/service)

    This segment is used to provide additional identification for products or devices.
    """
    produkt_erzeugnisnummer_qualifier: Optional[str] = None  # Function of the product ID
    waren_leistungsnummer_identifikation: Optional[WarenLeistungsnummerIdentifikation] = None  # Product/service ID


class SegmentQTY(BaseModel):
    """
    QTY-Segment (Quantity / Mengenelement)

    Specifies a quantity value with its unit of measurement.

    This segment is primarily used in MSCONS message types and includes:
    - Quantity qualifier (identifies the type of quantity)
    - Quantity (the actual quantity value)
    - Unit of measurement code (identifies the unit of measurement)

    Common qualifiers include:
    - '220': Measured value of the tariff period (Wahrer Wert)
    - '67': Substitute value (Ersatzwert)

    Common units include:
    - 'KWH': Kilowatt-hour
    - 'KWT': Kilowatt
    - 'D54': Watt/m²
    """
    menge_qualifier: Optional[str] = None  # e.g., '220' Wahrer Wert, '67' Ersatzwert
    menge: Optional[float] = None  # The quantity value
    masseinheit_code: Optional[str] = None  # e.g., 'KWH', 'KWT', 'D54'


class Statuskategorie(BaseModel):
    """
    Status category (Statuskategorie).

    Identifies the category of status information.

    According to MSCONS D.04B 2.4c, this includes:
    - Status category code (identifies the type of status category)

    Common codes include:
    - 'Z33': Plausibility hint (Plausibilisierungshinweis)
    """
    statuskategorie_code: Optional[str] = None  # e.g., 'Z33' Plausibilisierungshinweis


class Status(BaseModel):
    """
    Status (Status).

    Contains the actual status code.

    According to MSCONS D.04B 2.4c, this includes:
    - Status code (the actual status value)

    Common codes include:
    - 'Z83': Customer self-reading (Kundenselbstablesung)
    - 'Z84': Vacancy (Leerstand)
    """
    status_code: Optional[str] = None  # e.g., 'Z83' Kundenselbstablesung, 'Z84' Leerstand


class Statusanlass(BaseModel):
    """
    Status reason (Statusanlass).

    Identifies the reason for the status.

    According to MSCONS D.04B 2.4c, this includes:
    - Status reason code (identifies the reason for the status)

    Common codes include:
    - 'Z88': Comparative measurement (calibrated) (Vergleichsmessung (geeicht))
    - 'Z90': Measurement reconstruction from calibrated values (Messwertnachbildung aus geeichten Werten)
    - 'Z92': Interpolation (Interpolation)
    - 'Z93': Hold value (Haltewert)
    """
    statusanlass_code: Optional[str] = None  # e.g., 'Z88', 'Z90', 'Z92', 'Z93'


class SegmentSTS(BaseModel):
    """
    STS-Segment (Status / Statusangabe)

    Provides status information for the measurement value.

    According to MSCONS D.04B 2.4c, this segment includes:
    - Status category (identifies the type of status)
    - Status (the actual status value)
    - Status reason (identifies the reason for the status)

    This segment is used to provide information about plausibility, substitute value methods,
    correction reasons, gas quality, etc.
    """
    bezeichner: Optional[str] = None  # NON-EDIFACT custom technical field
    statuskategorie: Optional[Statuskategorie] = None  # Type of status
    status: Optional[Status] = None  # Actual status
    statusanlass: Optional[Statusanlass] = None  # Reason for status
