# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..converters import QTYSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentQTY


class QTYSegmentHandler(SegmentHandler[SegmentQTY], ABC):
    """
    Abstract handler for QTY (Quantity) segments.

    This handler processes QTY segments, which specify quantities for the current 
    item position, including the quantity value and unit of measurement. It updates 
    the parsing context with the converted QTY segment information, creating a new 
    segment group when needed.

    Specific implementations for different message types (e.g., MSCONS) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the QTY segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(QTYSegmentConverter(syntax_parser=syntax_parser))
