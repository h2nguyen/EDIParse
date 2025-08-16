import unittest

from ediparse.infrastructure.libs.edifactparser.converters.sts_segment_converter import STSSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.sts_segment_handler import MSCONSSTSSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments.segment_group import SegmentGroup10
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentSTS


class TestSTSSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSSTSSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSSTSSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = STSSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentSTS()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, STSSegmentConverter)

    def test_update_context_updates_context_correctly_for_sg10(self):
        """Test that _update_context updates the context correctly for SG10."""
        # Arrange
        current_segment_group = SegmentGroup.SG10
        self.context.current_sg10 = SegmentGroup10()

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIn(self.segment, self.context.current_sg10.sts_statusangaben)

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

    def test_handle_updates_context_with_converted_sts(self):
        """Handle should convert STS and update context in SG10 without mocks."""
        # Arrange
        line_number = 1
        element_components = ["STS", "Z34", "", "Z81"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG10
        self.context.current_sg10 = SegmentGroup10()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNotNone(self.context.current_sg10)
        self.assertGreaterEqual(len(self.context.current_sg10.sts_statusangaben), 1)

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["STS", "Z34", "", "Z81"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG10
        self.context.current_message = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNone(self.context.current_message)


if __name__ == '__main__':
    unittest.main()
