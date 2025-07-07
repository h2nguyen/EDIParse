# coding: utf-8

from abc import ABC, abstractmethod
from typing import Optional

from . import SegmentHandler
from ..converters import COMSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
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

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the COM segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(COMSegmentConverter(syntax_parser=syntax_parser))
