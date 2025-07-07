# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..converters import STSSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentSTS


class STSSegmentHandler(SegmentHandler[SegmentSTS], ABC):
    """
    Abstract handler for STS (Status) segments.

    This handler processes STS segments, which specify status information such as 
    correction reason, gas quality, replacement value formation procedure, or 
    plausibility note. It updates the parsing context with the converted STS 
    segment information, appending it to the appropriate collection.

    Specific implementations for different message types (e.g., MSCONS) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the STS segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(STSSegmentConverter(syntax_parser=syntax_parser))
