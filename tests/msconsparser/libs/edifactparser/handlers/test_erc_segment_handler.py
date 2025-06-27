import unittest
from unittest.mock import MagicMock

from ediparse.libs.edifactparser.converters import ERCSegmentConverter
from ediparse.libs.edifactparser.handlers import ERCSegmentHandler
from ediparse.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.libs.edifactparser.mods.aperak.segments import EdifactAperakMessage
from ediparse.libs.edifactparser.wrappers.segments import SegmentERC, Anwendungsfehler
from ediparse.libs.edifactparser.wrappers.constants import SegmentGroup


class TestERCSegmentHandler(unittest.TestCase):
    """Test case for the ERCSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = ERCSegmentHandler(syntax_parser=self.syntax_parser)
        self.context = APERAKParsingContext()
        self.context.current_message = EdifactAperakMessage()
        self.segment = SegmentERC(fehlercode=Anwendungsfehler(anwendungsfehler_code="E12"))

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct converter."""
        self.assertIsInstance(self.handler.converter, ERCSegmentConverter)

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
        result = self.handler._can_handle(self.context)

        # Assert
        self.assertTrue(result)

    def test_can_handle_returns_false_when_current_message_does_not_exist(self):
        """Test that _can_handle returns False when current_message does not exist."""
        # Arrange
        self.context.current_message = None

        # Act
        result = self.handler._can_handle(self.context)

        # Assert
        self.assertFalse(result)

    def test_handle_calls_convert_and_update_context(self):
        """Test that handle calls convert and _update_context."""
        # Arrange
        line_number = 1
        element_components = ["ERC", "E12"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG4

        # Mock the converter's convert method to return a known segment
        self.handler.converter.convert = MagicMock(return_value=self.segment)

        # Mock the _update_context method to verify it's called
        self.handler._update_context = MagicMock()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.handler.converter.convert.assert_called_once_with(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )
        self.handler._update_context.assert_called_once_with(self.segment, current_segment_group, self.context)


if __name__ == '__main__':
    unittest.main()
