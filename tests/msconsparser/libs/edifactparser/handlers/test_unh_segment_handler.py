import unittest
from unittest.mock import MagicMock

from ediparse.libs.edifactparser.converters import UNHSegmentConverter
from ediparse.libs.edifactparser.exceptions import EdifactParserException
from ediparse.libs.edifactparser.handlers.unh_segment_handler import UNHSegmentHandler
from ediparse.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.libs.edifactparser.wrappers.segments import EdifactInterchange, SegmentUNH


class TestUNHSegmentHandler(unittest.TestCase):
    """Test case for the UNHSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = UNHSegmentHandler(syntax_parser=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.interchange = EdifactInterchange()
        self.segment = SegmentUNH()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct converter."""
        self.assertIsInstance(self.handler.converter, UNHSegmentConverter)

    def test_update_context_raises_exception_when_nachrichten_kennung_is_none(self):
        """Test that _update_context raises an exception when nachrichten_kennung is None."""
        # Arrange
        current_segment_group = None
        self.segment.nachrichten_kennung = None

        # Act & Assert
        with self.assertRaises(EdifactParserException) as context:
            self.handler._update_context(self.segment, current_segment_group, self.context)

        self.assertEqual(str(context.exception), "nachrichten_kennung should not be None.")

    def test_can_handle_returns_true_when_interchange_exists(self):
        """Test that _can_handle returns True when interchange exists."""
        # Act
        result = self.handler._can_handle(self.context)

        # Assert
        self.assertTrue(result)

    def test_can_handle_returns_false_when_interchange_does_not_exist(self):
        """Test that _can_handle returns False when interchange does not exist."""
        # Arrange
        self.context.interchange = None

        # Act
        result = self.handler._can_handle(self.context)

        # Assert
        self.assertFalse(result)

    def test_handle_calls_convert_and_update_context(self):
        """Test that handle calls convert and _update_context."""
        # Arrange
        line_number = 1
        element_components = ["UNH", "12345", "MSCONS", "D", "96A", "UN", "EAN005"]
        last_segment_type = None
        current_segment_group = None

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

    def test_handle_does_not_call_convert_when_can_handle_returns_false(self):
        """Test that handle does not call convert when _can_handle returns False."""
        # Arrange
        line_number = 1
        element_components = ["UNH", "12345", "MSCONS", "D", "96A", "UN", "EAN005"]
        last_segment_type = None
        current_segment_group = None
        self.context.interchange = None  # This will make _can_handle return False

        # Mock the converter's convert method to verify it's not called
        self.handler.converter.convert = MagicMock()

        # Mock the _update_context method to verify it's not called
        self.handler._update_context = MagicMock()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.handler.converter.convert.assert_not_called()
        self.handler._update_context.assert_not_called()


if __name__ == '__main__':
    unittest.main()
