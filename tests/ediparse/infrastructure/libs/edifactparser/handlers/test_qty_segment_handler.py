import unittest

from ediparse.infrastructure.libs.edifactparser.converters.qty_segment_converter import QTYSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.qty_segment_handler import MSCONSQTYSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments.segment_group import SegmentGroup9, SegmentGroup10
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments.measurement import SegmentQTY


class TestQTYSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSQTYSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSQTYSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = QTYSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentQTY()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, QTYSegmentConverter)

    def test_update_context_updates_context_correctly_for_sg10(self):
        """Test that _update_context updates the context correctly for SG10."""
        # Arrange
        current_segment_group = SegmentGroup.SG10
        self.context.current_sg9 = SegmentGroup9()

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIsNotNone(self.context.current_sg10)
        self.assertEqual(self.segment, self.context.current_sg10.qty_mengenangaben)
        self.assertIn(self.context.current_sg10, self.context.current_sg9.sg10_mengen_und_statusangaben)

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

    def test_handle_updates_context_with_converted_qty(self):
        """Handle should convert QTY and update context in SG10 without mocks."""
        # Arrange
        line_number = 1
        element_components = ["QTY", "220:4.123:D54"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG10
        self.context.current_sg9 = SegmentGroup9()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNotNone(self.context.current_sg10)
        qty = self.context.current_sg10.qty_mengenangaben
        self.assertIsNotNone(qty)
        self.assertEqual(qty.menge_qualifier, "220")
        self.assertIsNotNone(qty.menge)
        self.assertEqual(qty.masseinheit_code, "D54")
        self.assertIn(self.context.current_sg10, self.context.current_sg9.sg10_mengen_und_statusangaben)

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["QTY", "220:4.123:D54"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG10
        self.context.current_message = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNone(self.context.current_message)


if __name__ == '__main__':
    unittest.main()
