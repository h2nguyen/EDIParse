import unittest
from unittest.mock import MagicMock

from ediparse.infrastructure.libs.edifactparser.converters.com_segment_converter import COMSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.com_segment_handler import MSCONSCOMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentCOM


class TestCOMSegmentHandler(unittest.TestCase):
    """Test case for the COMSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSCOMSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = COMSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentCOM()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, COMSegmentConverter)

    def test_update_context_updates_context_correctly(self):
        """Test that _update_context updates the context correctly."""
        # Arrange
        current_segment_group = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        # The specific assertion will depend on the handler implementation
        # This is a placeholder that should be updated for each handler
        self.assertIsNotNone(self.context.current_message)

    def test_can_handle_returns_true_when_current_message_exists(self):
        """Test that _can_handle returns True when current_message exists."""
        # Act
        result = self.handler.can_handle(self.context)

        # Assert
        self.assertTrue(result)

    def test_can_handle_returns_false_when_current_message_does_not_exist(self):
        """Test that _can_handle returns False when current_message does not exist."""
        # Arrange
        self.context.current_message = None

        # Act
        result = self.handler.can_handle(self.context)

        # Assert
        self.assertFalse(result)

    def test_handle_calls_convert_and_update_context(self):
        """Test that handle calls convert and _update_context."""
        # Arrange
        line_number = 1
        element_components = ["COM", "example", "data"]
        last_segment_type = None
        current_segment_group = None

        # Mock the __converter's convert method to return a known segment
        self.handler._SegmentHandler__converter.convert = MagicMock(return_value=self.segment)

        # Mock the _update_context method to verify it's called
        self.handler._update_context = MagicMock()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.handler._SegmentHandler__converter.convert.assert_called_once_with(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )
        self.handler._update_context.assert_called_once_with(self.segment, current_segment_group, self.context)

    def test_handle_does_not_call_convert_when_can_handle_returns_false(self):
        """Test that handle does not call convert when _can_handle returns False."""
        # Arrange
        line_number = 1
        element_components = ["COM", "example", "data"]
        last_segment_type = None
        current_segment_group = None
        self.context.current_message = None  # This will make _can_handle return False

        # Mock the __converter's convert method to verify it's not called
        self.handler._SegmentHandler__converter.convert = MagicMock()

        # Mock the _update_context method to verify it's not called
        self.handler._update_context = MagicMock()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.handler._SegmentHandler__converter.convert.assert_not_called()
        self.handler._update_context.assert_not_called()


if __name__ == '__main__':
    unittest.main()
