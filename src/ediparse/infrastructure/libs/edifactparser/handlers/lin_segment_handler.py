# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..converters import LINSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentLIN


class LINSegmentHandler(SegmentHandler[SegmentLIN], ABC):
    """
    Abstract handler for LIN (Line Item) segments.

    This handler processes LIN segments, which identify a line item and its configuration 
    in a message. It updates the parsing context with the converted LIN segment information, 
    creating a new segment group 9 when needed.

    Specific implementations for different message types (e.g., MSCONS) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the LIN segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(LINSegmentConverter(syntax_parser=syntax_parser))
