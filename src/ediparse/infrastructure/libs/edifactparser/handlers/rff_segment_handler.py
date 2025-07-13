# coding: utf-8

from abc import ABC

from . import SegmentHandler
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

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the RFF segment handler.

        The __converter will be auto-detected during the handle method execution based on the message type.
        If a message-type-specific __converter exists in the mods/<message-type>/converters directory,
        it will be used; otherwise, the default __converter will be used.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(
            syntax_helper=syntax_helper,
        )
