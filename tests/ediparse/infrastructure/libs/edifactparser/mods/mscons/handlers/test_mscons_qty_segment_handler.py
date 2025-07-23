import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.qty_segment_handler import MSCONSQTYSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import SegmentGroup9
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentQTY


class TestMSCONSQTYSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSQTYSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSQTYSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        # Set up segment groups needed for testing
        self.context.current_sg9 = SegmentGroup9()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSQTYSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg10(self):
        """Test the _update_context method with segment group SG10."""
        # Arrange
        segment = SegmentQTY(
            menge_qualifier="220",
            menge=123.45,
            masseinheit_code="KWH"
        )
        current_segment_group = SegmentGroup.SG10

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg10)
        self.assertEqual(self.context.current_sg10.qty_mengenangaben, segment)
        self.assertEqual(len(self.context.current_sg9.sg10_mengen_und_statusangaben), 1)
        self.assertEqual(self.context.current_sg9.sg10_mengen_und_statusangaben[0], self.context.current_sg10)

    def test_update_context_with_non_sg10(self):
        """Test the _update_context method with a segment group other than SG10."""
        # Arrange
        segment = SegmentQTY(
            menge_qualifier="220",
            menge=123.45,
            masseinheit_code="KWH"
        )
        current_segment_group = SegmentGroup.SG1  # Not SG10
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(getattr(self.context, 'current_sg10', None))
        self.assertEqual(len(self.context.current_sg9.sg10_mengen_und_statusangaben), 0)

    def test_handle_with_sg10(self):
        """Test the handle method with segment group SG10."""
        # Arrange
        line_number = 1
        element_components = ["QTY", "220:123.45:KWH"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG10

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg10)
        qty_segment = self.context.current_sg10.qty_mengenangaben
        self.assertEqual(qty_segment.menge_qualifier, "220")
        self.assertEqual(qty_segment.menge, 123.45)
        self.assertEqual(qty_segment.masseinheit_code, "KWH")
        self.assertEqual(len(self.context.current_sg9.sg10_mengen_und_statusangaben), 1)
        self.assertEqual(self.context.current_sg9.sg10_mengen_und_statusangaben[0], self.context.current_sg10)


if __name__ == '__main__':
    unittest.main()