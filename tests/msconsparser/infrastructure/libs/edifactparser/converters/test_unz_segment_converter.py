import unittest

from ediparse.infrastructure.libs.edifactparser.converters.unz_segment_converter import UNZSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentUNZ


class TestUNZSegmentConverter(unittest.TestCase):
    """Test case for the UNZSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.context = MSCONSParsingContext()
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = UNZSegmentConverter(syntax_helper=self.syntax_parser)

    def test_convert_internal(self):
        """Test the _convert_internal method."""
        # Arrange
        element_components = ["UNZ", "1", "ABC4711"]
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
        self.assertIsInstance(result, SegmentUNZ)
        self.assertEqual(result.datenaustauschzaehler, 1)
        self.assertEqual(result.datenaustauschreferenz, "ABC4711")

    def test_convert_with_exception_missing_components(self):
        """Test the convert method with an exception due to missing components."""
        # Arrange
        line_number = 1
        element_components = ["UNZ", "1"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(
                line_number=line_number,
                element_components=element_components,
                last_segment_type=last_segment_type,
                current_segment_group=current_segment_group,
                context=self.context
            )

    def test_convert_with_invalid_datenaustauschzaehler(self):
        """Test the convert method with an exception due to invalid datenaustauschzaehler."""
        # Arrange
        line_number = 1
        element_components = ["UNZ", "invalid", "ABC4711"]  # Invalid datenaustauschzaehler
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(
                line_number=line_number,
                element_components=element_components,
                last_segment_type=last_segment_type,
                current_segment_group=current_segment_group,
                context=self.context
            )


if __name__ == '__main__':
    unittest.main()
