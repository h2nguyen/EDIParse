# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentLOC


class LOCSegmentHandler(SegmentHandler[SegmentLOC], ABC):
    """
    Abstract handler for LOC (Location) segments.

    This handler processes LOC segments, which specify the identification to which 
    the data applies and when EEG transfer time series are transferred. It updates 
    the parsing context with the converted LOC segment information, creating or 
    updating segment group as needed.

    Specific implementations for different message types (e.g., MSCONS) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the LOC segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(
            syntax_helper=syntax_helper,
        )
