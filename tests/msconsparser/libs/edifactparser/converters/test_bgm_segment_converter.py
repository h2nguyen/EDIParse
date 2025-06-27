import unittest

from ediparse.libs.edifactparser.converters import BGMSegmentConverter
from ediparse.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.libs.edifactparser.wrappers.segments import SegmentBGM


class TestBGMSegmentConverter(unittest.TestCase):
    """Test case for the BGMSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = BGMSegmentConverter(syntax_parser=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["BGM", "7", "MSI5422", "9"]
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
        self.assertIsInstance(result, SegmentBGM)
        self.assertEqual(result.dokumenten_nachrichtenname.dokumentenname_code, "7")
        self.assertEqual(result.dokumenten_nachrichten_identifikation.dokumentennummer, "MSI5422")
        self.assertEqual(result.nachrichtenfunktion_code, "9")

    def test_convert_internal_without_nachrichtenfunktion_code(self):
        """Test the _convert_internal method without nachrichtenfunktion_code."""
        # Arrange
        element_components = ["BGM", "7", "MSI5422"]
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
        self.assertIsInstance(result, SegmentBGM)
        self.assertEqual(result.dokumenten_nachrichtenname.dokumentenname_code, "7")
        self.assertEqual(result.dokumenten_nachrichten_identifikation.dokumentennummer, "MSI5422")
        self.assertIsNone(result.nachrichtenfunktion_code)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["BGM"]  # Missing required components
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
