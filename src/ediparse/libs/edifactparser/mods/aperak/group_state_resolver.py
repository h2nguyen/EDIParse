# coding: utf-8
import logging
from typing import Optional

from ...wrappers.context import ParsingContext
from ...wrappers.constants import SegmentGroup, SegmentType
from ...resolvers.group_state_resolver import GroupStateResolver

logger = logging.getLogger(__name__)


class AperakGroupStateResolver(GroupStateResolver):
    """
    Resolver for determining segment groups in APERAK messages.

    This class implements the GroupStateResolver interface for APERAK messages,
    providing logic to determine which segment group a particular segment belongs to
    based on the segment type and current context. It follows the structure defined
    in the APERAK UN D.07B S3 2.1i standard.

    The resolver handles transitions between segment groups as different segment types
    are encountered during parsing, ensuring that segments are properly organized
    according to the APERAK message structure.
    """

    @staticmethod
    def resolve_and_get_segment_group(
            current_segment_type: str,
            current_segment_group: Optional[SegmentGroup],
            context: Optional[ParsingContext],
    ) -> Optional[SegmentGroup]:
        """
        Determines the segment group of an APERAK message based on the current segment type
        and the current segment group.

        Args:
            current_segment_type (str): The type of the current segment
            current_segment_group (Optional[SegmentGroup]): The current segment group
            context: The context to use for the resolver.

        Returns:
            Optional[SegmentGroup]: The determined segment group, or None if the segment type is empty
        """
        if not current_segment_type:
            logger.error(f"Error: Segment type '{current_segment_type}' not exist!")
            return None

        if current_segment_type.startswith(SegmentType.DTM):
            return current_segment_group

        if current_segment_type.startswith(SegmentType.RFF):
            if current_segment_group is None:
                return SegmentGroup.SG2
            if current_segment_group == SegmentGroup.SG2:
                return SegmentGroup.SG2
            if current_segment_group == SegmentGroup.SG4:
                return SegmentGroup.SG5
            if current_segment_group == SegmentGroup.SG5:
                return SegmentGroup.SG5

        if current_segment_type.startswith(SegmentType.NAD):
            return SegmentGroup.SG3

        if current_segment_type.startswith(SegmentType.CTA):
            return SegmentGroup.SG3

        if current_segment_type.startswith(SegmentType.COM):
            return SegmentGroup.SG3

        if current_segment_type.startswith(SegmentType.ERC):
            return SegmentGroup.SG4

        if current_segment_type.startswith(SegmentType.FTX):
            if current_segment_group is None:
                return SegmentGroup.SG4
            if current_segment_group is SegmentGroup.SG4:
                return SegmentGroup.SG4
            if current_segment_group == SegmentGroup.SG5:
                return SegmentGroup.SG5

        return None
