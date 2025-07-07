# coding: utf-8

from abc import ABC

from . import SegmentHandler
from ..converters import UNHSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.segments.message import SegmentUNH


class UNHSegmentHandler(SegmentHandler[SegmentUNH], ABC):
    """
    Abstract handler for UNH (Message Header) segments.

    This handler processes UNH segments, which are used to head, identify, and specify 
    a message. It updates the parsing context with the converted UNH segment information, 
    creating a new message and resetting the context for processing a new message.

    Specific implementations for different message types (e.g., MSCONS, APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the UNH segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(UNHSegmentConverter(syntax_parser=syntax_parser))

    def can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.
        UNH segments can always be handled if the interchange exists.

        Args:
            context: The parsing context to check.

        Returns:
            True if the context is valid, False otherwise.
        """
        return context.interchange is not None
