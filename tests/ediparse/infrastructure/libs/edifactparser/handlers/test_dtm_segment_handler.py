import unittest

from ediparse.infrastructure.libs.edifactparser.converters.dtm_segment_converter import DTMSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.dtm_segment_handler import MSCONSDTMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import EdifactMSconsMessage
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments.segment_group import (
    SegmentGroup1 as MscSG1,
    SegmentGroup6 as MscSG6,
    SegmentGroup10 as MscSG10,
)
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentDTM


class TestDTMSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSDTMSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSDTMSegmentHandler(syntax_helper=self.syntax_parser)
        # Initialize the converter attribute for testing
        self.handler._SegmentHandler__converter = DTMSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentDTM()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct __converter."""
        self.assertIsInstance(self.handler._SegmentHandler__converter, DTMSegmentConverter)

    def test_update_context_updates_context_correctly_for_header(self):
        """Test that _update_context updates the context correctly for the header."""
        # Arrange
        current_segment_group = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIn(self.segment, self.context.current_message.dtm_nachrichtendatum)

    def test_update_context_updates_context_correctly_for_sg1(self):
        """Test that _update_context updates the context correctly for SG1."""
        # Arrange
        current_segment_group = SegmentGroup.SG1
        self.context.current_sg1 = MscSG1()

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIn(self.segment, self.context.current_sg1.dtm_versionsangabe_marktlokationsscharfe_allokationsliste_gas_mmma)

    def test_update_context_updates_context_correctly_for_sg6(self):
        """Test that _update_context updates the context correctly for SG6."""
        # Arrange
        current_segment_group = SegmentGroup.SG6
        self.context.current_sg6 = MscSG6()

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIn(self.segment, self.context.current_sg6.dtm_zeitraeume)

    def test_update_context_updates_context_correctly_for_sg10(self):
        """Test that _update_context updates the context correctly for SG10."""
        # Arrange
        current_segment_group = SegmentGroup.SG10
        self.context.current_sg10 = MscSG10()

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        self.assertIn(self.segment, self.context.current_sg10.dtm_zeitangaben)

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

    def test_handle_updates_header_context_with_converted_dtm(self):
        """Handle should convert DTM and update header context without mocks."""
        # Arrange
        line_number = 1
        element_components = ["DTM", "137:20210601:102"]
        last_segment_type = None
        current_segment_group = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertGreaterEqual(len(self.context.current_message.dtm_nachrichtendatum), 1)
        dtm = self.context.current_message.dtm_nachrichtendatum[-1]
        self.assertEqual(dtm.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "137")
        self.assertEqual(dtm.datum_oder_uhrzeit_oder_zeitspanne_wert, "20210601")
        self.assertEqual(dtm.datums_oder_uhrzeit_oder_zeitspannen_format_code, "102")

    def test_handle_noop_when_can_handle_returns_false(self):
        """When context is invalid, handle should do nothing (no mocks)."""
        # Arrange
        line_number = 1
        element_components = ["DTM", "137:20210601:102"]
        last_segment_type = None
        current_segment_group = None
        self.context.current_message = None

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Verify
        self.assertIsNone(self.context.current_message)


if __name__ == '__main__':
    unittest.main()
