import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.rff_segment_handler import MSCONSRFFSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import SegmentGroup6
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentRFF


class TestMSCONSRFFSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSRFFSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSRFFSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        # Set up segment groups needed for testing
        self.context.current_sg6 = SegmentGroup6()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSRFFSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg1(self):
        """Test the _update_context method with segment group SG1."""
        # Arrange
        segment = SegmentRFF(
            referenz_qualifier="Z13",
            referenz_identifikation="13025"
        )
        current_segment_group = SegmentGroup.SG1

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg1)
        self.assertEqual(self.context.current_sg1.rff_referenzangaben, segment)
        self.assertEqual(len(self.context.current_message.sg1_referenzen), 1)
        self.assertEqual(self.context.current_message.sg1_referenzen[0], self.context.current_sg1)

    def test_update_context_with_sg7(self):
        """Test the _update_context method with segment group SG7."""
        # Arrange
        segment = SegmentRFF(
            referenz_qualifier="23",
            referenz_identifikation="12345678"
        )
        current_segment_group = SegmentGroup.SG7

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg7)
        self.assertEqual(self.context.current_sg7.rff_referenzangabe, segment)
        self.assertEqual(len(self.context.current_sg6.sg7_referenzangaben), 1)
        self.assertEqual(self.context.current_sg6.sg7_referenzangaben[0], self.context.current_sg7)

    def test_update_context_with_non_sg1_sg7(self):
        """Test the _update_context method with a segment group other than SG1 or SG7."""
        # Arrange
        segment = SegmentRFF(
            referenz_qualifier="Z13",
            referenz_identifikation="13025"
        )
        current_segment_group = SegmentGroup.SG2  # Not SG1 or SG7
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(getattr(self.context, 'current_sg1', None))
        self.assertEqual(len(self.context.current_message.sg1_referenzen), 0)
        self.assertIsNone(getattr(self.context, 'current_sg7', None))
        self.assertEqual(len(self.context.current_sg6.sg7_referenzangaben), 0)

    def test_handle_with_sg1(self):
        """Test the handle method with segment group SG1."""
        # Arrange
        line_number = 1
        element_components = ["RFF", "Z13:13025"]
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
        self.assertIsNotNone(self.context.current_sg1)
        rff_segment = self.context.current_sg1.rff_referenzangaben
        self.assertEqual(rff_segment.referenz_qualifier, "Z13")
        self.assertEqual(rff_segment.referenz_identifikation, "13025")
        self.assertEqual(len(self.context.current_message.sg1_referenzen), 1)
        self.assertEqual(self.context.current_message.sg1_referenzen[0], self.context.current_sg1)

    def test_handle_with_sg7(self):
        """Test the handle method with segment group SG7."""
        # Arrange
        line_number = 1
        element_components = ["RFF", "23:12345678"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG7

        # Act
        self.handler.handle(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg7)
        rff_segment = self.context.current_sg7.rff_referenzangabe
        self.assertEqual(rff_segment.referenz_qualifier, "23")
        self.assertEqual(rff_segment.referenz_identifikation, "12345678")
        self.assertEqual(len(self.context.current_sg6.sg7_referenzangaben), 1)
        self.assertEqual(self.context.current_sg6.sg7_referenzangaben[0], self.context.current_sg7)


if __name__ == '__main__':
    unittest.main()