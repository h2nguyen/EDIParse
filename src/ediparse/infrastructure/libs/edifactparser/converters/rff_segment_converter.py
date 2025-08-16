# coding: utf-8
from typing import Optional

from . import SegmentConverter
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup
from ..wrappers.segments import SegmentRFF


class RFFSegmentConverter(SegmentConverter[SegmentRFF]):
    """
    Abstract __converter for RFF (Reference) segments.

    This __converter transforms RFF segment data from EDIFACT format into a structured
    SegmentRFF object. The RFF segment is used to specify reference information, such as 
    verification identifier, configuration ID, device number, or previous master data
    message of the Metering Point Operator (MSB).

    Specific implementations for different message types (e.g., MSCONS, APERAK) should be
    provided in their respective mods folders.
    """

    def __init__(self, syntax_helper: EdifactSyntaxHelper):
        """
        Initialize the RFF segment __converter with the syntax parser.

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
    ) -> SegmentRFF:
        """
        Converts RFF (Reference) segment components to a SegmentRFF object.

        The RFF segment is used to specify the reference information, e.g.: verification identifier,
        configuration ID, the device number, or previous master data message of the Metering Point Operator (MSB)

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the __converter.

        Returns:
            SegmentRFF object with function qualifier, reference qualifier, and identification

        Examples:
        RFF+AGI:AFN9523'
        """
        details = self._syntax_parser.split_components(
            string_content=element_components[1],
            context=context,
        )
        qualifier = details[0]
        identification = details[1] if len(details) > 1 else None

        return SegmentRFF(
            bezeichner=self._get_identifier_name(
                qualifier_code=qualifier,
                current_segment_group=current_segment_group,
                context=context
            ),
            referenz_qualifier=qualifier,
            referenz_identifikation=identification
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> Optional[str]:
        """
        Maps RFF qualifier codes to human-readable identifier names for APERAK messages.

        This method provides specific mappings for reference qualifier codes to meaningful
        names that describe their purpose in APERAK messages, taking into account the current
        segment group context.

        Args:
            qualifier_code: The reference qualifier code from the RFF segment
            current_segment_group: The current segment group being processed
            context: The parsing context containing the message type and segment group context information

        Returns:
            A human-readable identifier name for the reference, or None if no mapping exists
        """
        if qualifier_code == "ACW":
            return "Referenznummer einer vorangegangenen Nachricht"
        return super()._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=context
        )