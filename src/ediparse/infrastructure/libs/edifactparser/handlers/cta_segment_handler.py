# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..converters import CTASegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentCTA


class CTASegmentHandler(SegmentHandler[SegmentCTA], ABC):
    """
    Abstract handler for CTA (Contact Information) segments.

    This handler processes CTA segments, which identify a person or department to whom 
    communication should be directed. It updates the parsing context with the converted 
    CTA segment information, creating a new segment group when needed.

    Specific implementations for different message types (e.g., MSCONS, APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the CTA segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(CTASegmentConverter(syntax_parser=syntax_parser))
