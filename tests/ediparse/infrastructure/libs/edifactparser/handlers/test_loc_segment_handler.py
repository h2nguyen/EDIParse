import unittest

from ediparse.infrastructure.libs.edifactparser.converters.loc_segment_converter import LOCSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.loc_segment_handler import MSCONSLOCSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments.segment_group import SegmentGroup5
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentLOC


class TestLOCSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSLOCSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSLOCSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = LOCSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentLOC()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, LOCSegmentConverter)

    def test_update_context_updates_context_correctly_for_sg6(self):
        """Test that _update_context updates the context correctly for SG6."""
        # Arrange
        current_segment_group = SegmentGroup.SG6
        self.context.current_sg5 = SegmentGroup5()
        self.context.current_sg6 = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIsNotNone(self.context.current_sg6)
        self.assertEqual(self.segment, self.context.current_sg6.loc_identifikationsangabe)
        self.assertIn(self.context.current_sg6, self.context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt)

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

    def test_handle_updates_context_with_converted_loc(self):
        """Handle should convert LOC and update context in SG6 without mocks."""
        # Arrange
        line_number = 1
        element_components = ["LOC", "237", "11XUENBSOLS----X"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG6
        self.context.current_sg5 = SegmentGroup5()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNotNone(self.context.current_sg6)
        loc = self.context.current_sg6.loc_identifikationsangabe
        self.assertIsNotNone(loc)
        self.assertEqual(loc.ortsangabe_qualifier, "237")
        self.assertIn(self.context.current_sg6, self.context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt)

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["LOC", "237", "11XUENBSOLS----X"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG6
        self.context.current_message = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNone(self.context.current_message)


if __name__ == '__main__':
    unittest.main()
