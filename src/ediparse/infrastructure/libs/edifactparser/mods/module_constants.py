# coding: utf-8
"""
Constants for EDIFACT message types.

This module defines the EDIFACT message types supported by the parser.
These constants are used throughout the codebase to identify different
types of EDIFACT messages and their specific parsing requirements.
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


class EdifactMessageType(StrEnum):
    """
    The EDIFACT message types supported by the parser.
    """
    APERAK = "APERAK"
    MSCONS = "MSCONS"

    # Add more EDIFACT message types as needed...