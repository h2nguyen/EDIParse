# coding: utf-8
"""
Abstract base class for EDIFACT segment group resolvers.

This module defines the interface for resolvers that determine which segment group
a particular segment belongs to during EDIFACT message parsing. Different message
types (MSCONS, APERAK, etc.) have different segment group structures, so each
requires its own implementation of this interface.
"""

from abc import ABC
from typing import Optional

from ..wrappers.constants import SegmentGroup
from ..wrappers.context import ParsingContext


class GroupStateResolver(ABC):
    """
    Abstract base class for segment group resolvers.

    This class defines the interface for resolvers that determine the segment group
    context during EDIFACT message parsing. Concrete implementations analyze the
    current segment type and parsing context to determine which segment group a
    segment belongs to, ensuring that segments are properly organized according to
    the specific message type's structure.

    Different message types (MSCONS, APERAK, etc.) have different segment group
    structures and rules for transitioning between groups, so each requires its
    own implementation of this interface.
    """

    @staticmethod
    def resolve_and_get_segment_group(
            current_segment_type: str,
            current_segment_group: Optional[SegmentGroup],
            context: Optional[ParsingContext],
    ) -> Optional[SegmentGroup]:
        """
        Determines the segment group of a message type based on the current segment type and
        the current segment group.

        Args:
            current_segment_type (str): The type of the current segment
            current_segment_group (Optional[SegmentGroup]): The current segment group
            context: The context to use for the resolver.

        Returns:
            Optional[SegmentGroup]: The determined segment group, or None if the segment type is empty
        """
        pass
