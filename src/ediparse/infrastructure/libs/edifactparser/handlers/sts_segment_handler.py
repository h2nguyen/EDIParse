# coding: utf-8

from abc import ABC

from . import SegmentHandler
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

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the STS segment handler.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        # The __converter will be provided by the message-specific implementation
        super().__init__(
            syntax_helper=syntax_helper,
        )
