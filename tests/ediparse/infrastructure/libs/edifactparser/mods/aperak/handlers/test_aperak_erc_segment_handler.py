import unittest

from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.erc_segment_handler import APERAKERCSegmentHandler
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentERC, Anwendungsfehler


class TestAPERAKERCSegmentHandler(unittest.TestCase):
    """Test case for the APERAKERCSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = APERAKERCSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = APERAKParsingContext()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = APERAKERCSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg4(self):
        """Test the _update_context method with segment group SG4."""
        # Arrange
        segment = SegmentERC(
            fehlercode=Anwendungsfehler(anwendungsfehler_code="Z18")
        )
        current_segment_group = SegmentGroup.SG4

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg4)
        self.assertEqual(self.context.current_sg4.erc_error_code, segment)
        self.assertEqual(len(self.context.current_message.sg4_fehler_beschreibung), 1)
        self.assertEqual(self.context.current_message.sg4_fehler_beschreibung[0], self.context.current_sg4)

    def test_update_context_with_non_sg4(self):
        """Test the _update_context method with a segment group other than SG4."""
        # Arrange
        segment = SegmentERC(
            fehlercode=Anwendungsfehler(anwendungsfehler_code="Z18")
        )
        current_segment_group = SegmentGroup.SG2  # Not SG4
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(self.context.current_sg4)
        self.assertEqual(len(self.context.current_message.sg4_fehler_beschreibung), 0)

    def test_handle_with_sg4(self):
        """Test the handle method with segment group SG4."""
        # Arrange
        line_number = 1
        element_components = ["ERC", "Z10"]
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
        self.assertIsNotNone(self.context.current_sg4)
        erc_segment = self.context.current_sg4.erc_error_code
        self.assertEqual(erc_segment.fehlercode.anwendungsfehler_code, "Z10")
        self.assertEqual(len(self.context.current_message.sg4_fehler_beschreibung), 1)
        self.assertEqual(self.context.current_message.sg4_fehler_beschreibung[0], self.context.current_sg4)


if __name__ == '__main__':
    unittest.main()