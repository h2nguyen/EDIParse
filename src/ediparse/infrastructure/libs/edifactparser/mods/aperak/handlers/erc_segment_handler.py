# coding: utf-8

from typing import Optional

from ....handlers.erc_segment_handler import ERCSegmentHandler
from ....mods.aperak.segments import SegmentGroup4
from ....utils import EdifactSyntaxHelper
from ....wrappers.context import ParsingContext
from ....wrappers.constants import SegmentGroup
from ....wrappers.segments import SegmentERC


class APERAKERCSegmentHandler(ERCSegmentHandler):
    """
    APERAK-specific handler for ERC (Application Error Detail) segments.

    This handler processes ERC segments in APERAK messages, which contain error codes.
    ERC segments are used to indicate specific issues encountered during message processing.
    The handler updates the parsing context by adding the segment to the appropriate segment group.

    In APERAK messages, ERC segments are used in segment group SG4 to provide error codes and details.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the APERAK ERC segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser)

    def _update_context(self, segment: SegmentERC, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted ERC segment.
        The update creates a new SG4 segment group and adds the ERC segment to it.

        Args:
            segment: The converted ERC segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG4 == current_segment_group:
            context.current_sg4 = SegmentGroup4()
            context.current_sg4.erc_error_code = segment
            context.current_message.sg4_fehler_beschreibung.append(context.current_sg4)
