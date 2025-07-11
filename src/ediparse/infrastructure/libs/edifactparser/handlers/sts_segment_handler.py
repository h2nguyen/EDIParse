# coding: utf-8

from typing import Optional

from . import SegmentHandler
from ..converters import STSSegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentSTS


class STSSegmentHandler(SegmentHandler[SegmentSTS]):
    """
    Handler for STS (Status) segments.

    This handler processes STS segments, which specify status information such as 
    correction reason, gas quality, replacement value formation procedure, or 
    plausibility note. It updates the parsing context with the converted STS 
    segment information, appending it to the appropriate collection.

    Currently, this handler supports MSCONS messages, where STS segments are used in
    segment group SG10 to provide status information.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the STS segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(STSSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentSTS, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted STS segment.
        The update depends on the current segment group.

        Args:
            segment: The converted STS segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG10 == current_segment_group:
            context.current_sg10.sts_statusangaben.append(segment)
