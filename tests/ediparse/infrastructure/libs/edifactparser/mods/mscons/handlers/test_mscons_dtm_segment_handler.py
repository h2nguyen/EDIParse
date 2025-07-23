import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.dtm_segment_handler import MSCONSDTMSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import SegmentGroup1, SegmentGroup6, SegmentGroup10
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentDTM


class TestMSCONSDTMSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSDTMSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSDTMSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        # Set up segment groups needed for testing
        self.context.current_sg1 = SegmentGroup1()
        self.context.current_sg6 = SegmentGroup6()
        self.context.current_sg10 = SegmentGroup10()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSDTMSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_no_segment_group(self):
        """Test the _update_context method with no segment group."""
        # Arrange
        segment = SegmentDTM(
            datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier="137",
            datum_oder_uhrzeit_oder_zeitspanne_wert="202507230756"
        )
        current_segment_group = None

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_message.dtm_nachrichtendatum), 1)
        self.assertEqual(self.context.current_message.dtm_nachrichtendatum[0], segment)

    def test_update_context_with_sg1(self):
        """Test the _update_context method with segment group SG1."""
        # Arrange
        segment = SegmentDTM(
            datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier="137",
            datum_oder_uhrzeit_oder_zeitspanne_wert="202507230756"
        )
        current_segment_group = SegmentGroup.SG1

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg1.dtm_versionsangabe_marktlokationsscharfe_allokationsliste_gas_mmma), 1)
        self.assertEqual(self.context.current_sg1.dtm_versionsangabe_marktlokationsscharfe_allokationsliste_gas_mmma[0], segment)

    def test_update_context_with_sg6(self):
        """Test the _update_context method with segment group SG6."""
        # Arrange
        segment = SegmentDTM(
            datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier="137",
            datum_oder_uhrzeit_oder_zeitspanne_wert="202507230756"
        )
        current_segment_group = SegmentGroup.SG6

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg6.dtm_zeitraeume), 1)
        self.assertEqual(self.context.current_sg6.dtm_zeitraeume[0], segment)

    def test_update_context_with_sg10(self):
        """Test the _update_context method with segment group SG10."""
        # Arrange
        segment = SegmentDTM(
            datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier="137",
            datum_oder_uhrzeit_oder_zeitspanne_wert="202507230756"
        )
        current_segment_group = SegmentGroup.SG10

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg10.dtm_zeitangaben), 1)
        self.assertEqual(self.context.current_sg10.dtm_zeitangaben[0], segment)

    def test_update_context_with_unknown_segment_group(self):
        """Test the _update_context method with an unknown segment group."""
        # Arrange
        segment = SegmentDTM(
            datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier="137",
            datum_oder_uhrzeit_oder_zeitspanne_wert="202507230756"
        )
        current_segment_group = SegmentGroup.SG2  # Not handled by DTM handler

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_message.dtm_nachrichtendatum), 0)
        self.assertEqual(len(self.context.current_sg1.dtm_versionsangabe_marktlokationsscharfe_allokationsliste_gas_mmma), 0)
        self.assertEqual(len(self.context.current_sg6.dtm_zeitraeume), 0)
        self.assertEqual(len(self.context.current_sg10.dtm_zeitangaben), 0)

    def test_handle_with_no_segment_group(self):
        """Test the handle method with no segment group."""
        # Arrange
        line_number = 1
        element_components = ["DTM", "137:202507230756:203"]
        last_segment_type = None
        current_segment_group = None

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_message.dtm_nachrichtendatum), 1)
        dtm_segment = self.context.current_message.dtm_nachrichtendatum[0]
        self.assertEqual(dtm_segment.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "137")
        self.assertIsNotNone(dtm_segment.datum_oder_uhrzeit_oder_zeitspanne_wert)

    def test_handle_with_sg1(self):
        """Test the handle method with segment group SG1."""
        # Arrange
        line_number = 1
        element_components = ["DTM", "137:202507230756:203"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG1

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(len(self.context.current_sg1.dtm_versionsangabe_marktlokationsscharfe_allokationsliste_gas_mmma), 1)
        dtm_segment = self.context.current_sg1.dtm_versionsangabe_marktlokationsscharfe_allokationsliste_gas_mmma[0]
        self.assertEqual(dtm_segment.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "137")
        self.assertIsNotNone(dtm_segment.datum_oder_uhrzeit_oder_zeitspanne_wert)


if __name__ == '__main__':
    unittest.main()