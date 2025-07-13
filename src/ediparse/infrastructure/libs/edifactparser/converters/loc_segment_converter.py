# coding: utf-8

from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import (
    SegmentLOC, Ortsangabe, ZugehoerigerOrt1Identifikation
)


class LOCSegmentConverter(SegmentConverter[SegmentLOC]):
    """
    Converter for LOC (Location) segments.

    This __converter transforms LOC segment data from EDIFACT format into a structured
    SegmentLOC object. The LOC segment is used to specify the identification to which 
    the data applies and when EEG transfer time series are transferred.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the LOC segment __converter with the syntax parser.

        Args:
            syntax_helper: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_helper=syntax_helper)

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> SegmentLOC:
        """
        Converts LOC (Identification information / balancing group) segment components to a SegmentLOC object.

        The LOC segment is used to specify the identification to which the data applies and when EEG transfer
        time series are transferred.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the __converter.

        Returns:
            SegmentLOC object with location information

        Examples:
        LOC+237+11XUENBSOLS----X+11XVNBSOLS-----X'
        LOC+107+11YR000000011247'
        LOC+172+DE00014559929E00856996N5139699L01'
        LOC+Z04+H0'
        """
        ortsangabe_qualifier = element_components[1]
        ortsangabe_code = element_components[2] if len(element_components) > 2 else None
        erster_zugehoeriger_platz_ort_code = element_components[3] if len(element_components) > 3 else None

        return SegmentLOC(
            ortsangabe_qualifier=ortsangabe_qualifier,
            ortsangabe=Ortsangabe(
                ortsangabe_code=ortsangabe_code
            ) if ortsangabe_code else None,
            zugehoeriger_ort_1_identifikation=ZugehoerigerOrt1Identifikation(
                erster_zugehoeriger_platz_ort_code=erster_zugehoeriger_platz_ort_code
            ) if erster_zugehoeriger_platz_ort_code else None,
        )
