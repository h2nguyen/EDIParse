import unittest

from ediparse.infrastructure.libs.edifactparser.converters.lin_segment_converter import LINSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.lin_segment_handler import MSCONSLINSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments.segment_group import SegmentGroup6
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentLIN


class TestLINSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSLINSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSLINSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = LINSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentLIN()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, LINSegmentConverter)

    def test_update_context_sets_lin_in_sg9_and_appends_to_sg6(self):
        """_update_context should set LIN on current SG9 and append SG9 to SG6 list when group is SG9."""
        # Arrange
        from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments.segment_group import SegmentGroup9
        current_segment_group = SegmentGroup.SG9
        self.context.current_sg6 = SegmentGroup6()

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Verify
        self.assertIsNotNone(self.context.current_sg9)
        self.assertEqual(self.context.current_sg9.lin_lfd_position, self.segment)
        self.assertIn(self.context.current_sg9, self.context.current_sg6.sg9_positionsdaten)

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

    def test_handle_updates_context_with_converted_lin(self):
        """Handle should convert LIN and update context in SG9 without mocks."""
        # Arrange
        line_number = 1
        element_components = ["LIN", "1"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG9
        self.context.current_sg6 = SegmentGroup6()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNotNone(self.context.current_sg9)
        lin = self.context.current_sg9.lin_lfd_position
        self.assertIsNotNone(lin)
        self.assertEqual(lin.positionsnummer, "1")
        self.assertIn(self.context.current_sg9, self.context.current_sg6.sg9_positionsdaten)

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["LIN", "1"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG9
        self.context.current_message = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNone(self.context.current_message)


if __name__ == '__main__':
    unittest.main()
