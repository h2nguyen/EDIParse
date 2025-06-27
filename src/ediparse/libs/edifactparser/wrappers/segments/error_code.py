# coding: utf-8
"""
Models related to error reporting in the APERAK message (ERC, FTX).

These models represent error codes and free text information in the APERAK message.
According to the APERAK UN D.07B S3 2.1i standard, these segments are used to report
errors and provide additional information about the location of the errors.
"""

from typing import Optional

from pydantic import BaseModel


class Anwendungsfehler(BaseModel):
    """
    Application error (Anwendungsfehler).

    Contains the error code that identifies the type of error.

    According to APERAK UN D.07B S3 2.1i, this includes:
    - Application error code (the specific error code)
    """
    anwendungsfehler_code: Optional[str] = None  # Specific error code


class TextReferenz(BaseModel):
    """
    Text reference (Text-Referenz).

    Contains a code that identifies the type of free text.
    """
    freier_text_code: str  # Code identifying the type of free text


class Text(BaseModel):
    """
    Text (Text).

    Contains free text information, typically describing an error or providing
    additional information about the location of an error.

    According to APERAK UN D.07B S3 2.1i, this includes:
    - Mandatory free text (primary text information)
    - Optional free text (additional text information)
    """
    freier_text_m: str  # Mandatory free text
    freier_text_c: Optional[str] = None  # Optional free text


class SegmentERC(BaseModel):
    """
    ERC-Segment (Error Code / Fehlercode)

    Identifies the type of error that occurred during message processing.

    According to APERAK UN D.07B S3 2.1i, this segment includes:
    - Error code (identifies the specific error)

    Different APERAKs are possible due to varied validations.
    """
    fehlercode: Anwendungsfehler  # Error code information


class SegmentFTX(BaseModel):
    """
    FTX-Segment (Free Text / Freitext)

    Provides additional information about an error, typically specifying
    the location where the error reported in the ERC segment occurs.

    According to APERAK UN D.07B S3 2.1i, this segment includes:
    - Text subject qualifier (identifies the purpose of the text)
    - Text (the actual free text information)
    """
    textbezug_qualifier: Optional[str] = None  # Purpose of the text
    text: Optional[Text] = None  # Free text information
