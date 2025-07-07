# coding: utf-8
"""
Constants and enumerations for EDIFACT message structures.

This module defines constants, enumerations, and segment types used in parsing
EDIFACT messages, particularly for MSCONS (Metering Statistics and Consumption)
and APERAK (Application Error and Acknowledgement) message types.
"""

import sys
from enum import Enum

# --- Fallback implementation for StrEnum for Python < 3.11 ---
if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    class StrEnum(str, Enum):
        """
        Simple emulation of StrEnum for Python versions
        before 3.11 (values behave like strings).
        """
        pass


class EdifactConstants:
    """
    Constants for EDIFACT message processing.
    """
    DOT_DECIMAL = "."

    UNA_SEGMENT_MAX_LENGTH: int = 9
    MIN_SEGMENT_COUNT_OF_AN_EDIFACT_MESSAGE = 5

    # Default delimiters and specifiers according to the EDIFACT standard using in the UNA Segment
    DEFAULT_COMPONENT_SEPARATOR: str = ":"  # Default character that separates components within an element.
    DEFAULT_ELEMENT_SEPARATOR: str = "+"  # Default character that separates elements within a segment.
    DEFAULT_DECIMAL_MARK: str = "."  # Default character that specifies a decimal point in a numeric value, e.g. "2.1" or "2,1".
    DEFAULT_RELEASE_INDICATOR: str = "?"  # Default escape character used to include special characters in data, e.g. "+" or ":".
    DEFAULT_RESERVED_INDICATOR: str = " "  # Default character that marks reserved use of a component, currently it must be a space.
    DEFAULT_SEGMENT_TERMINATOR: str = "'"  # Default character that marks the end of a segment.

class SegmentGroup(StrEnum):
    """
    Segment groups in EDIFACT message structures.

    These segment groups are used in both MSCONS and APERAK message types,
    though not all groups are used in all message types.
    """
    SG1 = "SG1"
    SG2 = "SG2"
    SG3 = "SG3"
    SG4 = "SG4"
    SG5 = "SG5"
    SG6 = "SG6"
    SG7 = "SG7"
    SG8 = "SG8"
    SG9 = "SG9"
    SG10 = "SG10"


class SegmentType(StrEnum):
    """
    EDIFACT segment identifiers (MSCONS UN D.04B S3 2.4c, APERAK UN D.07B S3 2.1i).
    The German names are based on the official MSCONS and APERAK message description,
    see:
      - MSCONS -> https://bdew-mako.de/pdf/MSCONS_MIG_2_4c_20231024.pdf
      - APERAK -> https://bdew-mako.de/pdf/APERAK_MIG_2_1i_20240619.pdf
    """
    UNA = "UNA"  # Service String Advice: Defines the EDIFACT separators.
    UNB = "UNB"  # Interchange Header - Encloses the data exchange.
    UNZ = "UNZ"  # Interchange Trailer - Closing record of the interchange.
    UNH = "UNH"  # Message Header - Beginning of an MSCONS message.
    UNT = "UNT"  # Message Trailer - End of an MSCONS message.
    BGM = "BGM"  # Beginning of Message - Message type/reference.
    DTM = "DTM"  # Date/Time/Period, e.g., 137=Message time, 163/164=Interval start/end.
    RFF = "RFF"  # Reference, e.g., Z13=Process ID, 23=Device number, 24=Configuration ID.
    NAD = "NAD"  # Name and Address - Partner identification (MS/MR/DP) or delivery location.
    CTA = "CTA"  # Contact Information - Contact person (Qualifier IC).
    COM = "COM"  # Communication Contact, e.g., TE=Telephone, EM=E-mail.
    LOC = "LOC"  # Place/Location Identification - Balance group (16) or object (17).
    UNS = "UNS"  # Section Control - Separates header and detail section.
    LIN = "LIN"  # Line Item - Sequential position within the position group.
    PIA = "PIA"  # Additional Product ID - Additional product/device ID.
    QTY = "QTY"  # Quantity, e.g., 220 = Measured value of the tariff period.
    CCI = "CCI"  # Marking of the time series type (Composite Code Information).
    STS = "STS"  # Status - Plausibility, substitute value method, correction reason, gas quality, etc.
    ERC = "ERC"  # Error code - Different APERAKs possible due to varied validations.
    FTX = "FTX"  # Free text - Specifies the location where the error reported in the ERC segment occurs

    # Add more segments according to other MIGs as needed...
