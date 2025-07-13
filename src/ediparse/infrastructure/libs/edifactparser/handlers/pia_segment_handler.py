# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentPIA


class PIASegmentHandler(SegmentHandler[SegmentPIA], ABC):
    """
    Abstract handler for PIA (Product Identification) segments.

    This handler processes PIA segments, which specify the product identification 
    for the current item using the OBIS identifier or the medium. It updates the 
    parsing context with the converted PIA segment information.

    Specific implementations for different message types (e.g., MSCONS) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the PIA segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(
            syntax_helper=syntax_helper,
        )
