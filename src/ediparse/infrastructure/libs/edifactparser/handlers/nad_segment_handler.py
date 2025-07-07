# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentNAD


class NADSegmentHandler(SegmentHandler[SegmentNAD], ABC):
    """
    Abstract handler for NAD (Name and Address) segments.

    This handler processes NAD segments, which identify the market partners and 
    the delivery location. It updates the parsing context with the converted NAD 
    segment information, creating new segment groups as needed.

    Specific implementations for different message types (e.g., MSCONS, APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the NAD segment handler.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        # The converter will be provided by the message-specific implementation
        super().__init__(None)
