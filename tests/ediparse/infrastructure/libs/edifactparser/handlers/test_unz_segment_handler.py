import unittest

from ediparse.infrastructure.libs.edifactparser.converters import UNZSegmentConverter
from ediparse.infrastructure.libs.edifactparser.handlers.unz_segment_handler import UNZSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentUNZ
from ediparse.infrastructure.libs.edifactparser.wrappers.segments.message_structure import EdifactInterchange


class TestUNZSegmentHandler(unittest.TestCase):
    """Test case for the UNZSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = UNZSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = UNZSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentUNZ()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, UNZSegmentConverter)

    def test_update_context_updates_context_correctly(self):
        """Test that _update_context updates the context correctly."""
        # Arrange
        current_segment_group = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIsNotNone(self.context.current_message)

    def test_can_handle_returns_true_when_interchange_exists(self):
        """Test that _can_handle returns True when interchange exists."""
        # Act
        result = self.handler.can_handle(self.context)

        # Assert
        self.assertTrue(result)

    def test_can_handle_returns_false_when_interchange_does_not_exist(self):
        """Test that _can_handle returns False when interchange does not exist."""
        # Arrange
        self.context.interchange = None

        # Act
        result = self.handler.can_handle(self.context)

        # Assert
        self.assertFalse(result)

    def test_handle_updates_context_with_converted_unz(self):
        """Handle should convert UNZ and update interchange without mocks."""
        # Arrange
        line_number = 1
        element_components = ["UNZ", "1", "ABC4711"]
        last_segment_type = None
        current_segment_group = None
        # ensure interchange exists
        self.context.interchange = EdifactInterchange()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        unz = self.context.interchange.unz_nutzdaten_endsegment
        self.assertIsNotNone(unz)
        self.assertEqual(unz.datenaustauschzaehler, 1)
        self.assertEqual(unz.datenaustauschreferenz, "ABC4711")

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["UNZ", "1", "ABC4711"]
        last_segment_type = None
        current_segment_group = None
        self.context.interchange = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.assertIsNone(self.context.interchange)


if __name__ == '__main__':
    unittest.main()
