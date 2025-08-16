import unittest

from ediparse.infrastructure.libs.edifactparser.converters.unh_segment_converter import UNHSegmentConverter
from ediparse.infrastructure.libs.edifactparser.exceptions import EdifactParserException
from ediparse.infrastructure.libs.edifactparser.mods.module_constants import EdifactMessageType
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.unh_segment_handler import MSCONSUNHSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentUNH
from ediparse.infrastructure.libs.edifactparser.wrappers.segments.message_structure import EdifactInterchange


class TestUNHSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSUNHSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSUNHSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = UNHSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.interchange = EdifactInterchange()
        self.segment = SegmentUNH()
        # Set up a minimal nachrichten_kennung for the segment using SimpleNamespace
        from types import SimpleNamespace
        self.segment.nachrichten_kennung = SimpleNamespace(
            nachrichtentyp_kennung=EdifactMessageType.MSCONS
        )

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, UNHSegmentConverter)

    def test_update_context_raises_exception_when_nachrichten_kennung_is_none(self):
        """Test that _update_context raises an exception when nachrichten_kennung is None."""
        # Arrange
        current_segment_group = None
        self.segment.nachrichten_kennung = None

        # Act & Assert
        with self.assertRaises(EdifactParserException) as context:
            self.handler._update_context(self.segment, current_segment_group, self.context)

        self.assertEqual(str(context.exception), "nachrichten_kennung should not be None.")

    def test_update_context_creates_mscons_message(self):
        """Test that _update_context creates an MSCONS message."""
        # Arrange
        current_segment_group = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIsNotNone(self.context.current_message)
        self.assertIsInstance(self.context.current_message, EdifactMSconsMessage)
        self.assertEqual(self.segment, self.context.current_message.unh_nachrichtenkopfsegment)
        self.assertIn(self.context.current_message, self.context.interchange.unh_unt_nachrichten)
        self.assertEqual(self.context.message_type, EdifactMessageType.MSCONS)

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

    def test_handle_updates_context_with_converted_unh(self):
        """Handle should convert UNH and update context without mocks."""
        # Arrange
        line_number = 1
        element_components = ["UNH", "1", "MSCONS:D:04B:UN:2.4c"]
        last_segment_type = None
        current_segment_group = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNotNone(self.context.current_message)
        self.assertIsInstance(self.context.current_message, EdifactMSconsMessage)
        self.assertEqual(self.context.message_type, EdifactMessageType.MSCONS)
        self.assertEqual(self.context.current_message.unh_nachrichtenkopfsegment.nachrichten_referenznummer, "1")

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["UNH", "1", "MSCONS:D:04B:UN:2.4c"]
        last_segment_type = None
        current_segment_group = None
        self.context.interchange = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.assertIsNone(self.context.interchange)


if __name__ == '__main__':
    unittest.main()
