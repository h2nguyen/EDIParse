import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.com_segment_handler import MSCONSCOMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import SegmentGroup4
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentCOM, Kommunikationsverbindung


class TestMSCONSCOMSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSCOMSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSCOMSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_sg4 = SegmentGroup4()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSCOMSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg4(self):
        """Test the _update_context method with segment group SG4."""
        # Arrange
        segment = SegmentCOM(
            kommunikationsverbindung=Kommunikationsverbindung(
                kommunikationsadresse_identifikation="test@example.com",
                kommunikationsadresse_qualifier="EM"
            )
        )
        current_segment_group = SegmentGroup.SG4

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg4.com_kommunikationsverbindung), 1)
        self.assertEqual(self.context.current_sg4.com_kommunikationsverbindung[0], segment)

    def test_update_context_with_non_sg4(self):
        """Test the _update_context method with a segment group other than SG4."""
        # Arrange
        segment = SegmentCOM(
            kommunikationsverbindung=Kommunikationsverbindung(
                kommunikationsadresse_identifikation="test@example.com",
                kommunikationsadresse_qualifier="EM"
            )
        )
        current_segment_group = SegmentGroup.SG1  # Not SG4
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg4.com_kommunikationsverbindung), 0)

    def test_handle_with_sg4(self):
        """Test the handle method with segment group SG4."""
        # Arrange
        line_number = 1
        element_components = ["COM", "test@example.com:EM"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG4

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg4.com_kommunikationsverbindung), 1)
        com_segment = self.context.current_sg4.com_kommunikationsverbindung[0]
        self.assertEqual(com_segment.kommunikationsverbindung.kommunikationsadresse_identifikation, "test@example.com")
        self.assertEqual(com_segment.kommunikationsverbindung.kommunikationsadresse_qualifier, "EM")


if __name__ == '__main__':
    unittest.main()