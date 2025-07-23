import unittest

from ediparse.infrastructure.libs.edifactparser.converters.lin_segment_converter import LINSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentLIN


class TestLINSegmentConverter(unittest.TestCase):
    """Test case for the LINSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = LINSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_convert_internal(self):
        """Test the _convert_internal method."""
        # Arrange
        element_components = ["LIN", "1"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentLIN)
        self.assertEqual(result.positionsnummer, "1")

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["LIN"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(
                line_number=line_number,
                element_components=element_components,
                last_segment_type=last_segment_type,
                current_segment_group=current_segment_group,
                context=MSCONSParsingContext()
            )


if __name__ == '__main__':
    unittest.main()
