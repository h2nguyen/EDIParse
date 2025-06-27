# coding: utf-8
"""
Package containing wrapper classes for EDIFACT message segments.

This package provides classes that represent different types of EDIFACT segments
and their components. These classes are used to create structured object models
of parsed EDIFACT messages, making it easier to work with the data.

The segments are organized into categories:
- Base models: Abstract base classes for EDIFACT messages
- Error code models: Segments related to error reporting (ERC, FTX)
- Location models: Segments related to locations and places (LOC, CCI)
- Measurement models: Segments related to measurements and quantities (LIN, PIA, QTY, STS)
- Message models: Segments related to message structure (BGM, UNS, UNT, UNH)
- Message structure models: Segments related to interchange structure (UNA, UNB, UNZ)
- Partner models: Segments related to partners and contacts (NAD, CTA, COM)
- Reference models: Segments related to references and dates (DTM, RFF)
"""

# Import base models
from .base import AbstractEdifactMessage

# Import error code models
from .error_code import (
    SegmentERC, SegmentFTX, Anwendungsfehler, Text
)

# Import location models
from .location import (
    SegmentLOC, SegmentCCI, Merkmalsbeschreibung, Ortsangabe, ZugehoerigerOrt1Identifikation
)

# Import measurement models
from .measurement import (
    SegmentLIN, SegmentPIA, SegmentQTY, SegmentSTS, WarenLeistungsnummerIdentifikation,
    Statusanlass, Status, Statuskategorie
)

# Import message models
from .message import (
    SegmentBGM, SegmentUNS, SegmentUNT, SegmentUNH, DokumentenNachrichtenname,
    DokumentenNachrichtenIdentifikation, NachrichtenKennung, StatusDerUebermittlung
)

# Import message structure models
from .message_structure import (
    SegmentUNA, SegmentUNB, SegmentUNZ, EdifactInterchange,
    SyntaxBezeichner, Marktpartner, DatumUhrzeit
)

# Import partner models
from .partner import (
    SegmentNAD, SegmentCTA, SegmentCOM, Kommunikationsverbindung,
    AbteilungOderBearbeiter, IdentifikationDesBeteiligten
)

# Import reference models
from .reference import (
    SegmentDTM, SegmentRFF
)
