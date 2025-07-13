# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentUNS


class UNSSegmentHandler(SegmentHandler[SegmentUNS], ABC):
    """
    Abstract handler for UNS (Section Control) segments.

    This handler processes UNS segments, which are used to separate the header and 
    detail sections of a message. It updates the parsing context with the converted 
    UNS segment information.

    Specific implementations for different message types (e.g., MSCONS) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the UNS segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(
            syntax_helper=syntax_helper,
        )
