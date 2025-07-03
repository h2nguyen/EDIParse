# coding: utf-8
"""
Package for MSCONS message segment models.

This package contains classes that represent the structure of MSCONS messages
according to the MSCONS D.04B 2.4c standard. It includes:

- Message structure models: Classes representing the overall MSCONS message structure
- Segment group models: Classes representing the different segment groups in MSCONS messages,
  from SG1 through SG10, each with specific purposes in the message hierarchy

These models are used to build a structured representation of MSCONS messages during parsing,
organizing data such as references, market partners, locations, and measurements.
"""

# Import message structure models
from .message_structure import (
    EdifactMSconsMessage
)
# Import segment group models
from .segment_group import (
    SegmentGroup1, SegmentGroup2, SegmentGroup4,
    SegmentGroup5, SegmentGroup6, SegmentGroup7,
    SegmentGroup8, SegmentGroup9, SegmentGroup10
)
