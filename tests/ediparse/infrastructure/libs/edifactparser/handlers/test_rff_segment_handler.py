import unittest
from unittest.mock import MagicMock

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.rff_segment_handler import MSCONSRFFSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentRFF


class TestMSCONSRFFSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSRFFSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSRFFSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentRFF()

    def test_init_creates_without_converter(self):
        """Test that the handler initializes without a __converter."""
        self.assertIsNone(self.handler.__converter)

    def test_update_context_updates_context_correctly_for_sg1(self):
        """Test that _update_context updates the context correctly for SG1."""
        # Arrange
        current_segment_group = SegmentGroup.SG1
        self.context.current_sg1 = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIsNotNone(self.context.current_sg1)
        self.assertEqual(self.segment, self.context.current_sg1.rff_referenzangaben)
        self.assertIn(self.context.current_sg1, self.context.current_message.sg1_referenzen)

    def test_update_context_updates_context_correctly_for_sg7(self):
        """Test that _update_context updates the context correctly for SG7."""
        # Arrange
        current_segment_group = SegmentGroup.SG7
        self.context.current_sg7 = None
        self.context.current_sg6 = MagicMock()
        self.context.current_sg6.sg7_referenzangaben = []

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIsNotNone(self.context.current_sg7)
        self.assertEqual(self.segment, self.context.current_sg7.rff_referenzangabe)
        self.assertIn(self.context.current_sg7, self.context.current_sg6.sg7_referenzangaben)

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

    def test_handle_auto_detects_converter_and_calls_convert_and_update_context(self):
        """Test that handle auto-detects the __converter, calls convert, and _update_context."""
        # Arrange
        line_number = 1
        element_components = ["RFF", "example", "data"]
        last_segment_type = None
        current_segment_group = None

        # Mock the _auto_detect_converter method to set a mock __converter
        mock_converter = MagicMock()
        mock_converter.convert.return_value = self.segment

        def side_effect(context):
            self.handler.__converter = mock_converter

        self.handler.__auto_detect_converter = MagicMock(side_effect=side_effect)

        # Mock the _update_context method to verify it's called
        self.handler._update_context = MagicMock()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.handler.__auto_detect_converter.assert_called_once_with(self.context)
        mock_converter.convert.assert_called_once_with(
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
        element_components = ["RFF", "example", "data"]
        last_segment_type = None
        current_segment_group = None
        self.context.current_message = None  # This will make _can_handle return False

        # Mock the _auto_detect_converter method to verify it's not called
        self.handler.__auto_detect_converter = MagicMock()

        # Mock the _update_context method to verify it's not called
        self.handler._update_context = MagicMock()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.handler.__auto_detect_converter.assert_not_called()
        self.handler._update_context.assert_not_called()


if __name__ == '__main__':
    unittest.main()
