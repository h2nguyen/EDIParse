# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..converters import FTXSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentFTX


class FTXSegmentHandler(SegmentHandler[SegmentFTX], ABC):
    """
    Abstract handler for FTX (Free Text) segments.

    This handler processes FTX segments, which contain free-format text information.
    FTX segments are used to provide detailed descriptions or additional information
    in various message types. The handler updates the parsing context by adding the 
    segment to the appropriate segment group based on the message type.

    Specific implementations for different message types (e.g., APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the FTX segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(FTXSegmentConverter(syntax_parser=syntax_parser))
