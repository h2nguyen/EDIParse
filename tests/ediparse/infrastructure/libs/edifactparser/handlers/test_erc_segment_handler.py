import unittest

from ediparse.infrastructure.libs.edifactparser.converters.erc_segment_converter import ERCSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.erc_segment_handler import APERAKERCSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.segments import EdifactAperakMessage
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments.error_code import SegmentERC, Anwendungsfehler


class TestERCSegmentHandler(unittest.TestCase):
    """Test case for the APERAKERCSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = APERAKERCSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = ERCSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = APERAKParsingContext()
        self.context.current_message = EdifactAperakMessage()
        self.segment = SegmentERC(fehlercode=Anwendungsfehler(anwendungsfehler_code="E12"))

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, ERCSegmentConverter)

    def test_update_context(self):
        """Test that _update_context updates the context correctly."""
        # Arrange
        current_segment_group = SegmentGroup.SG4

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertEqual(self.segment, self.context.current_sg4.erc_error_code)
        self.assertIn(self.context.current_sg4, self.context.current_message.sg4_fehler_beschreibung)

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

    def test_handle_updates_context_with_converted_erc(self):
        """Handle should convert ERC and update context in SG4 without mocks."""
        # Arrange
        line_number = 1
        element_components = ["ERC", "E12"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG4

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNotNone(self.context.current_sg4)
        erc = self.context.current_sg4.erc_error_code
        self.assertIsNotNone(erc)
        self.assertEqual(erc.fehlercode.anwendungsfehler_code, "E12")
        self.assertIn(self.context.current_sg4, self.context.current_message.sg4_fehler_beschreibung)


if __name__ == '__main__':
    unittest.main()
