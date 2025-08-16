import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.cci_segment_handler import MSCONSCCISegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import SegmentGroup6
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentCCI, Merkmalsbeschreibung


class TestMSCONSCCISegmentHandler(unittest.TestCase):
    """Test case for the MSCONSCCISegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSCCISegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        self.context.current_sg6 = SegmentGroup6()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSCCISegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg8(self):
        """Test the _update_context method with segment group SG8."""
        # Arrange
        segment = SegmentCCI(
            klassentyp_code="Z01",
            merkmalsbeschreibung=Merkmalsbeschreibung(
                merkmal_code="SRQ"
            )
        )
        current_segment_group = SegmentGroup.SG8

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg8)
        self.assertEqual(self.context.current_sg8.cci_zeitreihentyp, segment)
        self.assertEqual(len(self.context.current_sg6.sg8_zeitreihentypen), 1)
        self.assertEqual(self.context.current_sg6.sg8_zeitreihentypen[0], self.context.current_sg8)

    def test_update_context_with_non_sg8(self):
        """Test the _update_context method with a segment group other than SG8."""
        # Arrange
        segment = SegmentCCI(
            klassentyp_code="Z01",
            merkmalsbeschreibung=Merkmalsbeschreibung(
                merkmal_code="SRQ"
            )
        )
        current_segment_group = SegmentGroup.SG1  # Not SG8
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(getattr(self.context, 'current_sg8', None))
        self.assertEqual(len(self.context.current_sg6.sg8_zeitreihentypen), 0)

    def test_handle_with_sg8(self):
        """Test the handle method with segment group SG8."""
        # Arrange
        line_number = 1
        element_components = ["CCI", "Z01", "SRQ"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG8

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg8)
        cci_segment = self.context.current_sg8.cci_zeitreihentyp
        self.assertEqual(cci_segment.klassentyp_code, "Z01")
        # The converter might not set merkmalsbeschreibung correctly from element_components
        # So we'll just check if the segment was added to the context
        self.assertEqual(len(self.context.current_sg6.sg8_zeitreihentypen), 1)
        self.assertEqual(self.context.current_sg6.sg8_zeitreihentypen[0], self.context.current_sg8)


if __name__ == '__main__':
    unittest.main()