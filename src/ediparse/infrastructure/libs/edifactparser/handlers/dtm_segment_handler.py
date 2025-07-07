# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..converters import DTMSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentDTM


class DTMSegmentHandler(SegmentHandler[SegmentDTM], ABC):
    """
    Abstract handler for DTM (Date/Time/Period) segments.

    This handler processes DTM segments, which specify dates, times, periods, and their 
    function within the message. It updates the parsing context with the converted DTM 
    segment information, appending it to the appropriate collection based on the current 
    segment group.

    Specific implementations for different message types (e.g., MSCONS, APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the DTM segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(DTMSegmentConverter(syntax_parser=syntax_parser))
