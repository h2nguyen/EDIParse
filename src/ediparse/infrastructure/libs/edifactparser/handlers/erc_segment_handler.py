# coding: utf-8
from abc import ABC

from . import SegmentHandler
from ..converters import ERCSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentERC


class ERCSegmentHandler(SegmentHandler[SegmentERC], ABC):
    """
    Abstract handler for ERC (Application Error Detail) segments.

    This handler processes ERC segments, which contain error codes that indicate specific
    issues encountered during message processing. It updates the parsing context by adding
    the segment to the appropriate segment group based on the message type.

    Specific implementations for different message types (e.g., APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the ERC segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(ERCSegmentConverter(syntax_parser=syntax_parser))
