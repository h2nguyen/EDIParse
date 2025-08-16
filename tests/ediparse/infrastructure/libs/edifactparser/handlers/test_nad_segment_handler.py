import unittest

from ediparse.infrastructure.libs.edifactparser.converters.nad_segment_converter import NADSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.nad_segment_handler import MSCONSNADSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentNAD


class TestNADSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSNADSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSNADSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = NADSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentNAD()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, NADSegmentConverter)

    def test_update_context_updates_context_correctly_for_sg2(self):
        """Test that _update_context updates the context correctly for SG2."""
        # Arrange
        current_segment_group = SegmentGroup.SG2
        self.context.current_sg2 = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIsNotNone(self.context.current_sg2)
        self.assertEqual(self.segment, self.context.current_sg2.nad_marktpartner)
        self.assertIn(self.context.current_sg2, self.context.current_message.sg2_marktpartnern)

    def test_update_context_updates_context_correctly_for_sg5(self):
        """Test that _update_context updates the context correctly for SG5."""
        # Arrange
        current_segment_group = SegmentGroup.SG5
        self.context.current_sg5 = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIsNotNone(self.context.current_sg5)
        self.assertEqual(self.segment, self.context.current_sg5.nad_name_und_adresse)
        self.assertIn(self.context.current_sg5, self.context.current_message.sg5_liefer_bzw_bezugsorte)

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

    def test_handle_updates_context_with_converted_nad_sg2(self):
        """Handle should convert NAD and update context in SG2 without mocks."""
        # Arrange
        line_number = 1
        element_components = ["NAD", "MS", "4012345678901:14:9"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG2

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNotNone(self.context.current_sg2)
        nad = self.context.current_sg2.nad_marktpartner
        self.assertIsNotNone(nad)
        self.assertEqual(nad.beteiligter_qualifier, "MS")
        self.assertIn(self.context.current_sg2, self.context.current_message.sg2_marktpartnern)

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["NAD", "MS", "4012345678901:14:9"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG2
        self.context.current_message = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNone(self.context.current_message)


if __name__ == '__main__':
    unittest.main()
