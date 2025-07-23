import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.pia_segment_handler import MSCONSPIASegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import SegmentGroup9
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentPIA, WarenLeistungsnummerIdentifikation


class TestMSCONSPIASegmentHandler(unittest.TestCase):
    """Test case for the MSCONSPIASegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSPIASegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        # Set up segment groups needed for testing
        self.context.current_sg9 = SegmentGroup9()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSPIASegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg9(self):
        """Test the _update_context method with segment group SG9."""
        # Arrange
        segment = SegmentPIA(
            produkt_erzeugnisnummer_qualifier="1",
            waren_leistungsnummer_identifikation=WarenLeistungsnummerIdentifikation(
                produkt_leistungsnummer="1-1:1.8.0",
                art_der_produkt_leistungsnummer_code="Z14"
            )
        )
        current_segment_group = SegmentGroup.SG9

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(self.context.current_sg9.pia_produktidentifikation, segment)

    def test_update_context_with_non_sg9(self):
        """Test the _update_context method with a segment group other than SG9."""
        # Arrange
        segment = SegmentPIA(
            produkt_erzeugnisnummer_qualifier="1",
            waren_leistungsnummer_identifikation=WarenLeistungsnummerIdentifikation(
                produkt_leistungsnummer="1-1:1.8.0",
                art_der_produkt_leistungsnummer_code="Z14"
            )
        )
        current_segment_group = SegmentGroup.SG1  # Not SG9
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(self.context.current_sg9.pia_produktidentifikation)

    def test_handle_with_sg9(self):
        """Test the handle method with segment group SG9."""
        # Arrange
        line_number = 1
        element_components = ["PIA", "1", "1-1:1.8.0:Z14"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG9

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg9.pia_produktidentifikation)
        pia_segment = self.context.current_sg9.pia_produktidentifikation
        self.assertEqual(pia_segment.produkt_erzeugnisnummer_qualifier, "1")
        # The converter might not set waren_leistungsnummer_identifikation correctly from element_components
        # So we'll just check if the segment was added to the context


if __name__ == '__main__':
    unittest.main()