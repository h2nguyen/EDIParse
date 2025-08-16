import unittest

from ediparse.infrastructure.libs.edifactparser.converters import UNTSegmentConverter
from ediparse.infrastructure.libs.edifactparser.handlers import UNTSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentUNT


class TestUNTSegmentHandler(unittest.TestCase):
    """Test case for the UNTSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = UNTSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = UNTSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentUNT()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, UNTSegmentConverter)

    def test_update_context_updates_context_correctly(self):
        """Test that _update_context updates the context correctly."""
        # Arrange
        current_segment_group = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
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

    def test_handle_updates_context_with_converted_unt(self):
        """Handle should convert UNT and update current message without mocks."""
        # Arrange
        line_number = 1
        element_components = ["UNT", "5", "1"]
        last_segment_type = None
        current_segment_group = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        unt = self.context.current_message.unt_nachrichtenendsegment
        self.assertIsNotNone(unt)
        self.assertEqual(unt.anzahl_der_segmente_in_einer_nachricht, 5)
        self.assertEqual(unt.nachrichten_referenznummer, "1")

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["UNT", "5", "1"]
        last_segment_type = None
        current_segment_group = None
        self.context.current_message = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.assertIsNone(self.context.current_message)


if __name__ == '__main__':
    unittest.main()
