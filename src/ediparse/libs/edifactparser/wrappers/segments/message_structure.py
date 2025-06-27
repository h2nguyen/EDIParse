# coding: utf-8
"""
Models for the complete MSCONS message structure.

These models represent the overall structure of MSCONS messages and interchanges.
According to the MSCONS D.04B 2.4c standard, an interchange can contain multiple
messages, and each message follows a specific structure with segment groups.
"""

import json
from typing import Optional, Union, Annotated
from pydantic import BaseModel, Field

from ...mods.aperak.segments.message_structure import EdifactAperakMessage
from ...mods.mscons.segments.message_structure import EdifactMSconsMessage


class SegmentUNA(BaseModel):
    """
    Models for the UNA segment (Service String Advice).
    The UNA segment, also known as the Service String Advice, is an optional header
    at the beginning of an EDIFACT message. It defines the special characters used
    as delimiters in the message, allowing the message parser to correctly interpret
    the structure and content. When present, it overrides the default delimiters
    defined by the EDIFACT standard.


    The UNA segment is always exactly 9 characters long and each position has a specific meaning:
    1. Position 1–3: Segment tag "UNA"
    2. Position 4: Component data element separator
    3. Position 5: Data element separator
    4. Position 6: Decimal notation mark
    5. Position 7: Release character (escape)
    6. Position 8: Reserved (usually space)
    7. Position 9: Segment terminator

    Attributes:
        component_separator: Character that separates components within an element.
        element_separator: Character that separates elements within a segment.
        decimal_mark: Character that specifies a decimal point in a numeric value
        release_character: Escape character used to include special characters in data
        reserved: Character that marks reserved use of a component
        segment_terminator: Character that marks the end of a segment.

    Example: UNA:+.? '
    """
    component_separator: str  # Position 4: Component separator, e.g. (:)
    element_separator: str  # Position 5: Data element separator, e.g. (+)
    decimal_mark: str  # Position 6: Decimal notation mark, e.g. (.)
    release_character: str  # Position 7: Release character, e.g. (?)
    reserved: str  # Position 8: Reserved, usually space, e.g. ( )
    segment_terminator: str  # Position 9: Segment terminator, e.g. (')


class SyntaxBezeichner(BaseModel):
    """
    Syntax identifier and version (Syntax-Kennung).

    Contains the EDIFACT syntax identifier (e.g., 'UNOC' for UN/ECE character set C)
    and the syntax version number (e.g., '3' for Version 3).
    """
    syntax_kennung: Optional[str] = Field(default=None)  # e.g., 'UNOC' for UN/ECE character set C
    syntax_versionsnummer: Optional[str] = Field(default=None)  # e.g., '3' for Version 3


class Marktpartner(BaseModel):
    """
    Market partner identification (Marktpartner).

    Contains the market partner identification number (MP-ID) and
    the qualifier for the participant designation (e.g., '14' for GS1).
    """
    marktpartneridentifikationsnummer: Optional[str] = Field(default=None)  # MP-ID of sender/receiver
    teilnehmerbezeichnung_qualifier: Optional[str] = Field(default=None)  # e.g., '14' for GS1, '500'/'502' for DE


class DatumUhrzeit(BaseModel):
    """
    Date and time of creation (Datum/Uhrzeit der Erstellung).

    Contains the date in format YYMMDD and time in format HHMM.
    """
    datum: Optional[str] = Field(default=None)  # Format: YYMMDD
    uhrzeit: Optional[str] = Field(default=None)  # Format: HHMM


class SegmentUNB(BaseModel):
    """
    UNB-Segment (Interchange Header / Nutzdaten-Kopfsegment)

    Contains information about sender/receiver address, date/time, etc.
    This is the first segment of an EDIFACT interchange and defines the
    communication partners and technical parameters.

    According to MSCONS D.04B 2.4c, this segment includes:
    - Syntax identifier and version
    - Sender identification
    - Receiver identification
    - Date and time of creation
    - Interchange reference
    - Application reference (e.g., 'EM' for energy quantity, 'TL' for load profile)
    - Test indicator
    """
    syntax_bezeichner: Optional[SyntaxBezeichner] = Field(default=None)
    absender_der_uebertragungsdatei: Optional[Marktpartner] = Field(default=None)
    empfaenger_der_uebertragungsdatei: Optional[Marktpartner] = Field(default=None)
    datum_uhrzeit_der_erstellung: Optional[DatumUhrzeit] = Field(default=None)
    datenaustauschreferenz: Optional[str] = Field(default=None)  # Unique reference to identify the file
    anwendungsreferenz: Optional[str] = Field(default=None)  # e.g., 'EM' for energy quantity, 'TL' for load profile
    test_kennzeichen: Optional[str] = Field(default=None)  # '1' if test transmission


class SegmentUNZ(BaseModel):
    """
    UNZ-Segment (Interchange Trailer / Nutzdaten-Endesegment)

    Closes the interchange and contains control information.
    This is the last segment of an EDIFACT interchange.

    According to MSCONS D.04B 2.4c, this segment includes:
    - The total number of messages in the interchange
    - The interchange reference (must match the reference in UNB)
    """
    datenaustauschzaehler: Optional[int] = Field(default=None)  # Total number of messages in the interchange
    datenaustauschreferenz: Optional[str] = Field(default=None)  # Must match DE0020 in the UNB segment


EdifactMessageUnion = Annotated[
    Union[
        EdifactAperakMessage,
        EdifactMSconsMessage,
    ],
    Field(discriminator="message_type")
]
"""
Discriminated Union for EDIFACT message types.

This uses Pydantic v2's Discriminated Unions feature to create a union type
that can automatically determine the correct message type during deserialization
based on the 'message_type' field.

The 'message_type' field acts as a discriminator, allowing the system to:
1. Deserialize JSON data into the correct message type
2. Maintain type safety when working with collections of different message types
3. Enable polymorphic behavior without explicit type checking

This pattern is used in the EdifactInterchange.unh_unt_nachrichten field to store
different types of EDIFACT messages in a single list while maintaining type information.
"""

class EdifactInterchange(BaseModel):
    """
    Combines all messages, framed by UNB...UNZ (Nutzdaten-Kopfsegment...Nutzdaten-Endesegment).

    According to MSCONS D.04B 2.4c, an interchange consists of:
    1. An optional service string advice (UNA)
    2. An interchange header (UNB)
    3. One or more EDIFACT messages (UNH...UNT)
    4. An interchange trailer (UNZ)

    The interchange serves as an envelope for one or more messages,
    providing information about the sender, receiver, and technical parameters.
    The UNA segment, when present, defines the special characters used as delimiters.

    Design Pattern:
    --------------
    This class uses the composition pattern to combine different types of EDIFACT messages
    within a single interchange. The 'unh_unt_nachrichten' field uses Pydantic v2's 
    Discriminated Unions feature (via EdifactMessageUnion) to store different message types
    in a single list while maintaining type information.

    This design provides flexibility by:
    1. Allowing an interchange to contain multiple message types (APERAK, MSCONS, etc.)
    2. Enabling easy addition of new message types without changing the interchange structure
    3. Maintaining type safety when working with messages of different types
    4. Ensuring proper JSON serialization of all message types

    The 'message_type' field in each message class serves as the discriminator,
    allowing the system to automatically determine the correct message type during
    deserialization.
    """
    una_service_string_advice: Optional[SegmentUNA] = Field(default=None)  # Service string advice
    unb_nutzdaten_kopfsegment: SegmentUNB = Field(default=None)  # Interchange header
    unh_unt_nachrichten: list[EdifactMessageUnion] = Field(default_factory=list)  # Messages
    unz_nutzdaten_endsegment: SegmentUNZ = Field(default=None)  # Interchange trailer

    def to_json(self) -> str:
        """
        Converts the interchange to a JSON string.

        Returns:
            str: A JSON representation of the interchange with all its messages and segments.
        """
        return json.dumps(self.model_dump(), indent=2, ensure_ascii=False, default=str)
