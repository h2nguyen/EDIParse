# coding: utf-8

from abc import ABC
from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import (
    SegmentNAD, IdentifikationDesBeteiligten
)


class NADSegmentConverter(SegmentConverter[SegmentNAD], ABC):
    """
    Abstract converter for NAD (Name and Address) segments.

    This converter transforms NAD segment data from EDIFACT format into a structured
    SegmentNAD object. The NAD segment is used to identify the market partners and 
    the delivery location.

    Specific implementations for different message types (e.g., MSCONS, APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the NAD segment converter with the syntax parser.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser=syntax_parser)

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> SegmentNAD:
        """
        Converts NAD (Name and Address) segment components to a SegmentNAD object.

        The NAD segment is used to identify the market partners and the delivery location.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentNAD object with function qualifier and either market partner or delivery location

        Examples:
        NAD+MS+9920455302123::293'
        NAD+MR+4012345678901::9'
        NAD+DP'
        """
        beteiligter_qualifier = element_components[1]
        identifikation_des_beteiligten = self._syntax_parser.split_components(
            string_content=element_components[2],
            context=context,
        ) if len(element_components) > 2 else None

        return SegmentNAD(
            bezeichner=self._get_identifier_name(
                qualifier_code=beteiligter_qualifier,
                current_segment_group=current_segment_group,
                context=context
            ),
            beteiligter_qualifier=beteiligter_qualifier,
            identifikation_des_beteiligten=IdentifikationDesBeteiligten(
                beteiligter_identifikation=identifikation_des_beteiligten[0],
                verantwortliche_stelle_fuer_die_codepflege_code=identifikation_des_beteiligten[2]
            ) if identifikation_des_beteiligten and len(identifikation_des_beteiligten) > 2 else None
        )
