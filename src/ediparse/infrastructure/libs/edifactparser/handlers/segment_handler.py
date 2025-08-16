# coding: utf-8

from abc import ABC, abstractmethod
import logging
from typing import Optional, TypeVar, Generic

from ..converters import SegmentConverter
from ..converters.segment_converter_factory import SegmentConverterFactory
from ..exceptions import EdifactParserException
from ..utils import EdifactSyntaxHelper
from ..wrappers.context import ParsingContext
from ..wrappers.constants import SegmentGroup

T = TypeVar('T')
logger = logging.getLogger(__name__)


class SegmentHandler(ABC, Generic[T]):
    """
    Abstract base class for EDIFACT segment handlers.

    This class defines the interface for handling EDIFACT segments during the parsing process.
    Each segment type (e.g., DTM, BGM, NAD) has its own handler implementation that inherits
    from this class and provides specific logic for updating the parsing context with the
    information extracted from that segment.

    The handler uses a __converter to transform the raw segment data into a structured domain
    model object, and then updates the parsing context accordingly. This separation of concerns
    allows for a clean architecture where converters handle data transformation and handlers
    manage context updates.

    The generic type parameter T represents the specific segment model type that 
    a concrete handler implementation will process.
    """

    def __init__(
            self,
            syntax_helper: EdifactSyntaxHelper,
            converter: Optional[SegmentConverter[T]] = None
    ):
        """
        Initialize the handler with a __converter for the specific segment type.

        Args:
            converter: The optional __converter to use for converting the segment data.
                      If None, a message-type-specific __converter will be auto-detected
                      during the handle method execution.
        """
        self.__converter_factory = SegmentConverterFactory(syntax_helper)
        self.__converter = converter

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

        # Auto-detect and use message-type-specific __converter if available
        if self.__converter is None:
            self.__auto_detect_converter(context)

        # Convert the segment
        segment = self.__converter.convert(
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

    def __auto_detect_converter(self, context: ParsingContext) -> None:
        """
        Auto-detect and use message-type-specific __converter if available.

        This method checks if a message-type-specific __converter exists for the current segment type
        and message type. If one exists, it sets self.__converter to that __converter. Otherwise,
        it falls back to the default __converter.

        Args:
            context: The parsing context, which contains information about the message type.
        """
        # Get the segment type from the class name
        # The class name should follow the pattern <MessageType><SegmentType>SegmentHandler or <SegmentType>SegmentHandler
        class_name = self.__class__.__name__
        if "SegmentHandler" in class_name:
            segment_type = class_name.replace("SegmentHandler", "")
            # If the class name starts with a message type (e.g., APERAK, MSCONS, etc.), remove it
            if context.message_type:
                message_type_name = context.message_type.value
                if segment_type.startswith(message_type_name):
                    segment_type = segment_type[len(message_type_name):]
        else:
            # If the class name doesn't follow the expected pattern, we can't determine the segment type
            logger.warning(
                f"Cannot determine segment type from class name '{class_name}'."
            )
            return

        # Use the factory to get the appropriate __converter
        converter = self.__converter_factory.get_converter(segment_type, context)
        if converter:
            self.__converter = converter
        else:
            raise EdifactParserException(
                f"No __converter found for segment type '{segment_type}' and message type '{context.message_type}'."
            )

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
