import unittest

from ediparse.infrastructure.libs.edifactparser.converters.unb_segment_converter import UNBSegmentConverter
from ediparse.infrastructure.libs.edifactparser.handlers.unb_segment_handler import UNBSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentUNB
from ediparse.infrastructure.libs.edifactparser.wrappers.segments.message_structure import EdifactInterchange


class TestUNBSegmentHandler(unittest.TestCase):
    """Test case for the UNBSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = UNBSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = UNBSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.interchange = EdifactInterchange()
        self.segment = SegmentUNB()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, UNBSegmentConverter)

    def test_update_context_sets_unb_nutzdaten_kopfsegment(self):
        """Test that _update_context sets the unb_nutzdaten_kopfsegment on the interchange."""
        # Arrange
        current_segment_group = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertEqual(self.context.interchange.unb_nutzdaten_kopfsegment, self.segment)

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

    def test_handle_updates_context_with_converted_unb(self):
        """Handle should convert UNB and update interchange without mocks."""
        # Arrange
        line_number = 1
        element_components = [
            "UNB",
            "UNOC:3",
            "4012345678901:14",
            "4012345678901:14",
            "200426:1151",
            "ABC4711",
            "",
            "TL",
            "",
            "",
            "",
            "1",
        ]
        last_segment_type = None
        current_segment_group = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        unb = self.context.interchange.unb_nutzdaten_kopfsegment
        self.assertIsNotNone(unb)
        self.assertEqual(unb.syntax_bezeichner.syntax_kennung, "UNOC")
        self.assertEqual(unb.syntax_bezeichner.syntax_versionsnummer, "3")
        self.assertEqual(unb.datenaustauschreferenz, "ABC4711")

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["UNB", "UNOC:3", "4012345678901:14", "4012345678901:14", "200426:1151", "ABC4711"]
        last_segment_type = None
        current_segment_group = None
        self.context.interchange = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNone(self.context.interchange)


if __name__ == '__main__':
    unittest.main()
