import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.nad_segment_handler import MSCONSNADSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import SegmentGroup5 as MscSG5
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentNAD, IdentifikationDesBeteiligten


class TestMSCONSNADSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSNADSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSNADSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSNADSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg2(self):
        """Test the _update_context method with segment group SG2."""
        # Arrange
        segment = SegmentNAD(
            bezeichner="MR",
            beteiligter_qualifier="MR",
            identifikation_des_beteiligten=IdentifikationDesBeteiligten(
                beteiligter_identifikation="9900204000002",
                verantwortliche_stelle_fuer_die_codepflege_code="293"
            )
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
        self.assertEqual(self.context.current_sg2.nad_marktpartner, segment)
        self.assertEqual(len(self.context.current_message.sg2_marktpartnern), 1)
        self.assertEqual(self.context.current_message.sg2_marktpartnern[0], self.context.current_sg2)

    def test_update_context_with_sg5(self):
        """Test the _update_context method with segment group SG5."""
        # Arrange
        segment = SegmentNAD(
            bezeichner="DP",
            beteiligter_qualifier="DP",
            identifikation_des_beteiligten=IdentifikationDesBeteiligten(
                beteiligter_identifikation="9900204000003",
                verantwortliche_stelle_fuer_die_codepflege_code="293"
            )
        )
        current_segment_group = SegmentGroup.SG5

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg5)
        self.assertEqual(self.context.current_sg5.nad_name_und_adresse, segment)
        self.assertEqual(len(self.context.current_message.sg5_liefer_bzw_bezugsorte), 1)
        self.assertEqual(self.context.current_message.sg5_liefer_bzw_bezugsorte[0], self.context.current_sg5)

    def test_update_context_with_sg5_existing(self):
        """Test the _update_context method with segment group SG5 when current_sg5 already exists."""
        # Arrange
        segment = SegmentNAD(
            bezeichner="DP",
            beteiligter_qualifier="DP",
            identifikation_des_beteiligten=IdentifikationDesBeteiligten(
                beteiligter_identifikation="9900204000003",
                verantwortliche_stelle_fuer_die_codepflege_code="293"
            )
        )
        current_segment_group = SegmentGroup.SG5
        self.context.current_sg5 = MscSG5()

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg5)
        self.assertEqual(self.context.current_sg5.nad_name_und_adresse, segment)
        self.assertEqual(len(self.context.current_message.sg5_liefer_bzw_bezugsorte), 1)
        self.assertEqual(self.context.current_message.sg5_liefer_bzw_bezugsorte[0], self.context.current_sg5)

    def test_update_context_with_non_sg2_sg5(self):
        """Test the _update_context method with a segment group other than SG2 or SG5."""
        # Arrange
        segment = SegmentNAD(
            bezeichner="MR",
            beteiligter_qualifier="MR",
            identifikation_des_beteiligten=IdentifikationDesBeteiligten(
                beteiligter_identifikation="9900204000002",
                verantwortliche_stelle_fuer_die_codepflege_code="293"
            )
        )
        current_segment_group = SegmentGroup.SG1  # Not SG2 or SG5
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(getattr(self.context, 'current_sg2', None))
        self.assertEqual(len(self.context.current_message.sg2_marktpartnern), 0)
        self.assertIsNone(getattr(self.context, 'current_sg5', None))
        self.assertEqual(len(self.context.current_message.sg5_liefer_bzw_bezugsorte), 0)

    def test_handle_with_sg2(self):
        """Test the handle method with segment group SG2."""
        # Arrange
        line_number = 1
        element_components = ["NAD", "MR", "9900204000002::293"]
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
        nad_segment = self.context.current_sg2.nad_marktpartner
        self.assertEqual(nad_segment.beteiligter_qualifier, "MR")
        self.assertEqual(nad_segment.identifikation_des_beteiligten.beteiligter_identifikation, "9900204000002")
        self.assertEqual(nad_segment.identifikation_des_beteiligten.verantwortliche_stelle_fuer_die_codepflege_code, "293")
        self.assertEqual(len(self.context.current_message.sg2_marktpartnern), 1)
        self.assertEqual(self.context.current_message.sg2_marktpartnern[0], self.context.current_sg2)

    def test_handle_with_sg5(self):
        """Test the handle method with segment group SG5."""
        # Arrange
        line_number = 1
        element_components = ["NAD", "DP", "9900204000003::293"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG5

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
        nad_segment = self.context.current_sg5.nad_name_und_adresse
        self.assertEqual(nad_segment.beteiligter_qualifier, "DP")
        self.assertEqual(nad_segment.identifikation_des_beteiligten.beteiligter_identifikation, "9900204000003")
        self.assertEqual(nad_segment.identifikation_des_beteiligten.verantwortliche_stelle_fuer_die_codepflege_code, "293")
        self.assertEqual(len(self.context.current_message.sg5_liefer_bzw_bezugsorte), 1)
        self.assertEqual(self.context.current_message.sg5_liefer_bzw_bezugsorte[0], self.context.current_sg5)


if __name__ == '__main__':
    unittest.main()