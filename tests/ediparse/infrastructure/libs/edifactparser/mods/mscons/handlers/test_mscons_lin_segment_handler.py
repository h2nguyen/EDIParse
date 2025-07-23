import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.lin_segment_handler import MSCONSLINSegmentHandler
from ediparse.infrastructure.libs.edifactparser.mods.mscons.segments import SegmentGroup6
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.constants import SegmentGroup
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentLIN


class TestMSCONSLINSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSLINSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSLINSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()
        # Set up segment groups needed for testing
        self.context.current_sg6 = SegmentGroup6()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSLINSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context_with_sg9(self):
        """Test the _update_context method with segment group SG9."""
        # Arrange
        segment = SegmentLIN(
            positionsnummer="1"
        )
        current_segment_group = SegmentGroup.SG9

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNotNone(self.context.current_sg9)
        self.assertEqual(self.context.current_sg9.lin_lfd_position, segment)
        self.assertEqual(len(self.context.current_sg6.sg9_positionsdaten), 1)
        self.assertEqual(self.context.current_sg6.sg9_positionsdaten[0], self.context.current_sg9)

    def test_update_context_with_non_sg9(self):
        """Test the _update_context method with a segment group other than SG9."""
        # Arrange
        segment = SegmentLIN(
            positionsnummer="1"
        )
        current_segment_group = SegmentGroup.SG1  # Not SG9
        
        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsNone(getattr(self.context, 'current_sg9', None))
        self.assertEqual(len(self.context.current_sg6.sg9_positionsdaten), 0)

    def test_handle_with_sg9(self):
        """Test the handle method with segment group SG9."""
        # Arrange
        line_number = 1
        element_components = ["LIN", "1"]
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
        self.assertIsNotNone(self.context.current_sg9)
        lin_segment = self.context.current_sg9.lin_lfd_position
        self.assertEqual(lin_segment.positionsnummer, "1")
        self.assertEqual(len(self.context.current_sg6.sg9_positionsdaten), 1)
        self.assertEqual(self.context.current_sg6.sg9_positionsdaten[0], self.context.current_sg9)


if __name__ == '__main__':
    unittest.main()