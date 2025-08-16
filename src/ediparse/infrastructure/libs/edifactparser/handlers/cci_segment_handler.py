# coding: utf-8
from abc import ABC

from . import SegmentHandler
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentCCI


class CCISegmentHandler(SegmentHandler[SegmentCCI], ABC):
    """
    Abstract handler for CCI (Characteristic/Class ID) segments.

    This handler processes CCI segments, which specify product characteristics
    and the data that defines those characteristics. It updates the parsing context
    with the converted CCI segment information, creating a new segment group 8 when needed.

    Specific implementations for different message types (e.g., MSCONS) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the CCI segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(
            syntax_helper=syntax_helper,
        )
