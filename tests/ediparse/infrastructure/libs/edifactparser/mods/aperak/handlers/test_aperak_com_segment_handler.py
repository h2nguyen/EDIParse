import unittest

from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.com_segment_handler import APERAKCOMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.segments import SegmentGroup3
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import Kommunikationsverbindung
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentCOM


class TestAPERAKCOMSegmentHandler(unittest.TestCase):
    """Test case for the APERAKCOMSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = APERAKCOMSegmentHandler(syntax_parser=self.syntax_parser)
        self.context = APERAKParsingContext()
        self.kommunikationsverbindung = Kommunikationsverbindung(
            kommunikationsadresse_identifikation="info@example.com",
            kommunikationsadresse_qualifier="EM"
        )

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = APERAKCOMSegmentHandler(syntax_parser=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg3(self):
        """Test the _update_context method with segment group SG3."""
        # Arrange
        segment = SegmentCOM(kommunikationsverbindung=self.kommunikationsverbindung)
        current_segment_group = SegmentGroup.SG3
        
        # We need to set up the SG3 context first
        from ediparse.infrastructure.libs.edifactparser.mods.aperak.segments import SegmentGroup3
        self.context.current_sg3 = SegmentGroup3()

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg3.com_kommunikationsverbindungen), 1)
        self.assertEqual(self.context.current_sg3.com_kommunikationsverbindungen[0], segment)

    def test_update_context_with_non_sg3(self):
        """Test the _update_context method with a segment group other than SG3."""
        # Arrange
        segment = SegmentCOM(kommunikationsverbindung=self.kommunikationsverbindung)
        current_segment_group = SegmentGroup.SG2  # Not SG3
        
        # We need to set up the SG3 context first to verify it's not modified
        from ediparse.infrastructure.libs.edifactparser.mods.aperak.segments import SegmentGroup3
        self.context.current_sg3 = SegmentGroup3()
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg3.com_kommunikationsverbindungen), 0)

    def test_handle_with_sg3(self):
        """Test the handle method with segment group SG3."""
        # Arrange
        line_number = 1
        element_components = ["COM", "info@example.com:EM"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG3
        self.context.current_sg3 = SegmentGroup3()

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg3.com_kommunikationsverbindungen), 1)
        com_segment = self.context.current_sg3.com_kommunikationsverbindungen[0]
        self.assertEqual(com_segment.kommunikationsverbindung.kommunikationsadresse_identifikation, "info@example.com")
        self.assertEqual(com_segment.kommunikationsverbindung.kommunikationsadresse_qualifier, "EM")


if __name__ == '__main__':
    unittest.main()