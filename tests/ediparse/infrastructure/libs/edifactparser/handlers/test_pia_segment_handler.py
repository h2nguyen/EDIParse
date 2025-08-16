import unittest

from ediparse.infrastructure.libs.edifactparser.converters.pia_segment_converter import PIASegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.pia_segment_handler import MSCONSPIASegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments.segment_group import SegmentGroup9
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentPIA


class TestPIASegmentHandler(unittest.TestCase):
    """Test case for the MSCONSPIASegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSPIASegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = PIASegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentPIA()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, PIASegmentConverter)

    def test_update_context_updates_context_correctly_for_sg9(self):
        """Test that _update_context updates the context correctly for SG9."""
        # Arrange
        current_segment_group = SegmentGroup.SG9
        self.context.current_sg9 = SegmentGroup9()

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertEqual(self.segment, self.context.current_sg9.pia_produktidentifikation)

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

    def test_handle_updates_context_with_converted_pia(self):
        """Handle should convert PIA and update context in SG9 without mocks."""
        # Arrange
        line_number = 1
        element_components = ["PIA", "5", "1-1:1.8.1"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG9
        self.context.current_sg9 = SegmentGroup9()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNotNone(self.context.current_sg9)
        pia = self.context.current_sg9.pia_produktidentifikation
        self.assertIsNotNone(pia)
        self.assertEqual(pia.produkt_erzeugnisnummer_qualifier, "5")
        self.assertIsNotNone(pia.waren_leistungsnummer_identifikation)

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["PIA", "5", "1-1:1.8.1"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG9
        self.context.current_message = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNone(self.context.current_message)


if __name__ == '__main__':
    unittest.main()
