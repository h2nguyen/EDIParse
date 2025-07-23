import unittest

from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.aperak.handlers.nad_segment_handler import APERAKNADSegmentHandler
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentNAD, IdentifikationDesBeteiligten


class TestAPERAKNADSegmentHandler(unittest.TestCase):
    """Test case for the APERAKNADSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = APERAKNADSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = APERAKParsingContext()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = APERAKNADSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg3(self):
        """Test the _update_context method with segment group SG3."""
        # Arrange
        segment = SegmentNAD(
            bezeichner="MR",
            beteiligter_qualifier="MR",
            identifikation_des_beteiligten=IdentifikationDesBeteiligten(
                beteiligter_identifikation="9900204000002",
                verantwortliche_stelle_fuer_die_codepflege_code="293"
            )
        )
        current_segment_group = SegmentGroup.SG3

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg3)
        self.assertEqual(self.context.current_sg3.nad_marktpartner, segment)
        self.assertEqual(len(self.context.current_message.sg3_marktpartnern), 1)
        self.assertEqual(self.context.current_message.sg3_marktpartnern[0], self.context.current_sg3)

    def test_update_context_with_non_sg3(self):
        """Test the _update_context method with a segment group other than SG3."""
        # Arrange
        segment = SegmentNAD(
            bezeichner="MR",
            beteiligter_qualifier="MR",
            identifikation_des_beteiligten=IdentifikationDesBeteiligten(
                beteiligter_identifikation="9900204000002",
                verantwortliche_stelle_fuer_die_codepflege_code="293"
            )
        )
        current_segment_group = SegmentGroup.SG2  # Not SG3
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(self.context.current_sg3)
        self.assertEqual(len(self.context.current_message.sg3_marktpartnern), 0)

    def test_handle_with_sg3(self):
        """Test the handle method with segment group SG3."""
        # Arrange
        line_number = 1
        element_components = ["NAD", "MR", "9900204000002::293"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG3

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg3)
        nad_segment = self.context.current_sg3.nad_marktpartner
        self.assertEqual(nad_segment.bezeichner, "MP-ID Empfänger")
        self.assertEqual(nad_segment.beteiligter_qualifier, "MR")
        self.assertEqual(nad_segment.identifikation_des_beteiligten.beteiligter_identifikation, "9900204000002")
        self.assertEqual(nad_segment.identifikation_des_beteiligten.verantwortliche_stelle_fuer_die_codepflege_code, "293")
        self.assertEqual(len(self.context.current_message.sg3_marktpartnern), 1)
        self.assertEqual(self.context.current_message.sg3_marktpartnern[0], self.context.current_sg3)


if __name__ == '__main__':
    unittest.main()