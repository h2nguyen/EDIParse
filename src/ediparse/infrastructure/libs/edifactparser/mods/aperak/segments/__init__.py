# coding: utf-8
"""
Package for APERAK message segment models.

This package contains classes that represent the structure of APERAK messages
according to the APERAK UN D.07B S3 2.1i standard. It includes:

- Message structure models: Classes representing the overall APERAK message structure
- Segment group models: Classes representing the different segment groups in APERAK messages

These models are used to build a structured representation of APERAK messages during parsing.
"""

# Import message structure models
from .message_structure import (
    EdifactAperakMessage
)

# Import group models
from .segment_group import (
    SegmentGroup2, SegmentGroup3, SegmentGroup4, SegmentGroup5
)
