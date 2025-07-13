# coding: utf-8
from abc import ABC

from . import SegmentHandler
from ..utils import EdifactSyntaxHelper
from ..wrappers.segments import SegmentCOM


class COMSegmentHandler(SegmentHandler[SegmentCOM], ABC):
    """
    Abstract handler for COM (Communication Contact) segments.

    This handler processes COM segments, which provide communication information 
    such as telephone numbers, email addresses, etc. It updates the parsing context
    with the converted COM segment information, appending it to the appropriate segment group.

    Specific implementations for different message types (e.g., MSCONS, APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the COM segment handler with the appropriate __converter.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(
            syntax_helper=syntax_helper,
        )
