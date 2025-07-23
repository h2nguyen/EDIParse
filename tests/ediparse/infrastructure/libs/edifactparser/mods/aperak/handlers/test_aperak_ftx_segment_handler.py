import unittest

from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.ftx_segment_handler import APERAKFTXSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.segments import SegmentGroup4, SegmentGroup5
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentFTX, Text


class TestAPERAKFTXSegmentHandler(unittest.TestCase):
    """Test case for the APERAKFTXSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = APERAKFTXSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = APERAKParsingContext()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = APERAKFTXSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg4(self):
        """Test the _update_context method with segment group SG4."""
        # Arrange
        segment = SegmentFTX(
            textbezug_qualifier="Z02",
            text=Text(freier_text_m="Referenz Vorgangsnummer")
        )
        current_segment_group = SegmentGroup.SG4

        self.context.current_sg4 = SegmentGroup4()

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(self.context.current_sg4.ftx_freier_text, segment)

    def test_update_context_with_sg5(self):
        """Test the _update_context method with segment group SG5."""
        # Arrange
        segment = SegmentFTX(
            textbezug_qualifier="Z02",
            text=Text(freier_text_m="Referenz Vorgangsnummer")
        )
        current_segment_group = SegmentGroup.SG5

        self.context.current_sg5 = SegmentGroup5()

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg5.ftx_referenz_texte), 1)
        self.assertEqual(self.context.current_sg5.ftx_referenz_texte[0], segment)

    def test_update_context_with_non_sg4_sg5(self):
        """Test the _update_context method with a segment group other than SG4 or SG5."""
        # Arrange
        segment = SegmentFTX(
            textbezug_qualifier="Z02",
            text=Text(freier_text_m="Referenz Vorgangsnummer")
        )
        current_segment_group = SegmentGroup.SG2  # Not SG4 or SG5

        self.context.current_sg4 = SegmentGroup4()
        self.context.current_sg5 = SegmentGroup5()
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(self.context.current_sg4.ftx_freier_text)
        self.assertEqual(len(self.context.current_sg5.ftx_referenz_texte), 0)

    def test_handle_with_sg4(self):
        """Test the handle method with segment group SG4."""
        # Arrange
        line_number = 1
        element_components = ["FTX", "AAO", "", "", "Die Marktlokation ist bei Netzbetreiber Gasverteilung AG:"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG4

        self.context.current_sg4 = SegmentGroup4()

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg4.ftx_freier_text)
        ftx_segment = self.context.current_sg4.ftx_freier_text
        self.assertEqual(ftx_segment.textbezug_qualifier, "AAO")
        self.assertEqual(ftx_segment.text.freier_text_m, "Die Marktlokation ist bei Netzbetreiber Gasverteilung AG")

    def test_handle_with_sg5(self):
        """Test the handle method with segment group SG5."""
        # Arrange
        line_number = 1
        element_components = ["FTX", "AAO", "", "", "Die Marktlokation ist bei Netzbetreiber Gasverteilung AG:ggf. weiterer Text"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG5

        self.context.current_sg5 = SegmentGroup5()

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg5.ftx_referenz_texte), 1)
        ftx_segment = self.context.current_sg5.ftx_referenz_texte[0]
        self.assertEqual(ftx_segment.textbezug_qualifier, "AAO")
        self.assertEqual(ftx_segment.text.freier_text_m, "Die Marktlokation ist bei Netzbetreiber Gasverteilung AG")
        self.assertEqual(ftx_segment.text.freier_text_c, "ggf. weiterer Text")


if __name__ == '__main__':
    unittest.main()