import unittest

from ediparse.libs.edifactparser.converters.cci_segment_converter import CCISegmentConverter
from ediparse.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.libs.edifactparser.wrappers.segments import SegmentCCI


class TestCCISegmentConverter(unittest.TestCase):
    """Test case for the CCISegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = CCISegmentConverter(syntax_parser=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["CCI", "15", "", "BI1"]
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
        self.assertIsInstance(result, SegmentCCI)
        self.assertEqual(result.klassentyp_code, "15")
        self.assertIsNotNone(result.merkmalsbeschreibung)
        self.assertEqual(result.merkmalsbeschreibung.merkmal_code, "BI1")

    def test_convert_internal_without_merkmal_code(self):
        """Test the _convert_internal method without merkmal_code."""
        # Arrange
        element_components = ["CCI", "15"]
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
        self.assertIsInstance(result, SegmentCCI)
        self.assertEqual(result.klassentyp_code, "15")
        self.assertIsNone(result.merkmalsbeschreibung)

    def test_convert_internal_with_empty_gemessene_dimension_code(self):
        """Test the _convert_internal method with empty gemessene_dimension_code."""
        # Arrange
        element_components = ["CCI", "15", ""]
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
        self.assertIsInstance(result, SegmentCCI)
        self.assertEqual(result.klassentyp_code, "15")
        self.assertIsNone(result.merkmalsbeschreibung)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["CCI"]  # Missing required components
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
