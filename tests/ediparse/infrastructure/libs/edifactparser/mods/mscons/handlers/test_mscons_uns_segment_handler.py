import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.handlers.uns_segment_handler import MSCONSUNSSegmentHandler
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentUNS


class TestMSCONSUNSSegmentHandler(unittest.TestCase):
    """Test case for the MSCONSUNSSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.handler = MSCONSUNSSegmentHandler(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_initialization(self):
        """Test the initialization of the handler."""
        # Arrange & Act
        handler = MSCONSUNSSegmentHandler(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(handler)

    def test_update_context(self):
        """Test the _update_context method."""
        # Arrange
        segment = SegmentUNS(
            abschnittskennung_codiert="D"
        )
        current_segment_group = None

        # Act
        self.handler._update_context(
            segment=segment,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(self.context.current_message.uns_abschnitts_kontrollsegment, segment)

    def test_handle(self):
        """Test the handle method."""
        # Arrange
        line_number = 1
        element_components = ["UNS", "D"]
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
        self.assertIsNotNone(self.context.current_message.uns_abschnitts_kontrollsegment)
        uns_segment = self.context.current_message.uns_abschnitts_kontrollsegment
        self.assertEqual(uns_segment.abschnittskennung_codiert, "D")


if __name__ == '__main__':
    unittest.main()