# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..converters import RFFSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentRFF


class RFFSegmentHandler(SegmentHandler[SegmentRFF], ABC):
    """
    Abstract handler for RFF (Reference) segments.

    This handler processes RFF segments, which specify reference information, such as 
    verification identifier, configuration ID, device number, or previous master data 
    message of the Metering Point Operator (MSB). It updates the parsing context with 
    the converted RFF segment information, creating new segment groups as needed.

    Specific implementations for different message types (e.g., MSCONS, APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the RFF segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(RFFSegmentConverter(syntax_parser=syntax_parser))
