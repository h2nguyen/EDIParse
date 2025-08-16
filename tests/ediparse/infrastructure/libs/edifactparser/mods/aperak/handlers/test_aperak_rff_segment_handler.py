import unittest

from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.rff_segment_handler import APERAKRFFSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.aperak.segments import SegmentGroup4
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentRFF


class TestAPERAKRFFSegmentHandler(unittest.TestCase):
    """Test case for the APERAKRFFSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = APERAKRFFSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = APERAKParsingContext()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = APERAKRFFSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg2(self):
        """Test the _update_context method with segment group SG2."""
        # Arrange
        segment = SegmentRFF(
            bezeichner="Nummer des zugehörigen Dokuments",
            referenz_qualifier="ACE",
            referenz_identifikation="12345"
        )
        current_segment_group = SegmentGroup.SG2

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg2)
        self.assertEqual(self.context.current_sg2.rff_referenzangaben, segment)
        self.assertEqual(len(self.context.current_message.sg2_referenzen), 1)
        self.assertEqual(self.context.current_message.sg2_referenzen[0], self.context.current_sg2)

    def test_update_context_with_sg5(self):
        """Test the _update_context method with segment group SG5."""
        # Arrange
        segment = SegmentRFF(
            bezeichner="Ortsangabe des AHB-Fehlers",
            referenz_qualifier="Z02",
            referenz_identifikation="67890"
        )
        current_segment_group = SegmentGroup.SG5

        self.context.current_sg4 = SegmentGroup4()

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg5)
        self.assertEqual(self.context.current_sg5.rff_referenz, segment)
        self.assertEqual(len(self.context.current_sg4.sg5_nachrichtenreferenzen), 1)
        self.assertEqual(self.context.current_sg4.sg5_nachrichtenreferenzen[0], self.context.current_sg5)

    def test_handle_with_sg2(self):
        """Test the handle method with segment group SG2."""
        # Arrange
        line_number = 1
        element_components = ["RFF", "ACE:12345"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG2

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg2)
        self.assertEqual(self.context.current_sg2.rff_referenzangaben.referenz_qualifier, "ACE")
        self.assertEqual(self.context.current_sg2.rff_referenzangaben.referenz_identifikation, "12345")
        self.assertEqual(len(self.context.current_message.sg2_referenzen), 1)
        self.assertEqual(self.context.current_message.sg2_referenzen[0], self.context.current_sg2)

    def test_handle_with_sg5(self):
        """Test the handle method with segment group SG5."""
        # Arrange
        line_number = 1
        element_components = ["RFF", "Z02:67890"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG5

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
        self.assertIsNotNone(self.context.current_sg5)
        self.assertEqual(self.context.current_sg5.rff_referenz.referenz_qualifier, "Z02")
        self.assertEqual(self.context.current_sg5.rff_referenz.referenz_identifikation, "67890")
        self.assertEqual(len(self.context.current_sg4.sg5_nachrichtenreferenzen), 1)
        self.assertEqual(self.context.current_sg4.sg5_nachrichtenreferenzen[0], self.context.current_sg5)


if __name__ == '__main__':
    unittest.main()