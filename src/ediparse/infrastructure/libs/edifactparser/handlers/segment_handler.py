# coding: utf-8

from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

from ..converters import SegmentConverter
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup

T = TypeVar('T')


class SegmentHandler(ABC, Generic[T]):
    """
    Abstract base class for EDIFACT segment handlers.

    This class defines the interface for handling EDIFACT segments during the parsing process.
    Each segment type (e.g., DTM, BGM, NAD) has its own handler implementation that inherits
    from this class and provides specific logic for updating the parsing context with the
    information extracted from that segment.

    The handler uses a converter to transform the raw segment data into a structured domain
    model object, and then updates the parsing context accordingly. This separation of concerns
    allows for a clean architecture where converters handle data transformation and handlers
    manage context updates.

    The generic type parameter T represents the specific segment model type that 
    a concrete handler implementation will process.
    """

    def __init__(self, converter: Optional[SegmentConverter[T]] = None):
        """
        Initialize the handler with a converter for the specific segment type.

        Args:
            converter: The optional converter to use for converting the segment data.
        """
        self.converter = converter

    def handle(
            self,
            line_number: int,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> None:
        """
        Handle a segment by converting it and updating the context.

        Args:
            line_number: The line number of the segment in the input file.
            element_components: The components of the segment.
            last_segment_type: The type of the previous segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        # Check if the context is valid for this handler
        if not self.can_handle(context):
            return

        # Convert the segment
        segment = self.converter.convert(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=context
        )

        # Update the context with the converted segment
        self._update_context(segment, current_segment_group, context)

    def can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.

        Args:
            context: The parsing context to check.

        Returns:
            True if the context is valid, False otherwise.
        """
        # Default behavior for handling when the current context message exists.
        return context.current_message is not None

    @abstractmethod
    def _update_context(self, segment: T, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted segment.

        Args:
            segment: The converted segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        pass
