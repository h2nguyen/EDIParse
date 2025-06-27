import unittest

from ediparse.libs.edifactparser.converters import UNTSegmentConverter
from ediparse.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.libs.edifactparser.wrappers.segments import SegmentUNT


class TestUNTSegmentConverter(unittest.TestCase):
    """Test case for the UNTSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.context = MSCONSParsingContext()
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = UNTSegmentConverter(syntax_parser=self.syntax_parser)

    def test_convert_internal(self):
        """Test the _convert_internal method."""
        # Arrange
        element_components = ["UNT", "39", "1"]
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
        self.assertIsInstance(result, SegmentUNT)
        self.assertEqual(result.anzahl_der_segmente_in_einer_nachricht, 39)
        self.assertEqual(result.nachrichten_referenznummer, "1")

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["UNT", "39"]  # Missing required components
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

    def test_convert_with_invalid_segment_count(self):
        """Test the convert method with invalid segment count."""
        # Arrange
        line_number = 1
        element_components = ["UNT", "invalid", "1"]  # Invalid segment count
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
