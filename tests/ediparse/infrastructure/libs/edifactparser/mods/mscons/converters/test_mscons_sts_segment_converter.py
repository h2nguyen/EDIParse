import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.converters.sts_segment_converter import \
    MSCONSSTSSegmentConverter
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentSTS


class TestMSCONSSTSSegmentConverter(unittest.TestCase):
    """Test case for the MSCONSSTSSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = MSCONSSTSSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_initialization(self):
        """Test the initialization of the converter."""
        # Arrange & Act
        converter = MSCONSSTSSegmentConverter(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(converter)
        self.assertEqual(converter._syntax_parser, self.syntax_parser)

    def test_get_identifier_name_with_10_qualifier(self):
        """Test the _get_identifier_name method with 10 qualifier code."""
        # Arrange
        qualifier_code = "10"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Grundlage der Energiemenge")

    def test_get_identifier_name_with_z31_qualifier(self):
        """Test the _get_identifier_name method with Z31 qualifier code."""
        # Arrange
        qualifier_code = "Z31"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Gasqualität")

    def test_get_identifier_name_with_z32_qualifier(self):
        """Test the _get_identifier_name method with Z32 qualifier code."""
        # Arrange
        qualifier_code = "Z32"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Ersatzwertbildungsverfahren")

    def test_get_identifier_name_with_z33_qualifier(self):
        """Test the _get_identifier_name method with Z33 qualifier code."""
        # Arrange
        qualifier_code = "Z33"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Plausibilisierungshinweis")

    def test_get_identifier_name_with_z34_qualifier(self):
        """Test the _get_identifier_name method with Z34 qualifier code."""
        # Arrange
        qualifier_code = "Z34"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Korrekturgrund")

    def test_get_identifier_name_with_z40_qualifier(self):
        """Test the _get_identifier_name method with Z40 qualifier code."""
        # Arrange
        qualifier_code = "Z40"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Grund der Ersatzwertbildung")

    def test_get_identifier_name_with_unknown_qualifier(self):
        """Test the _get_identifier_name method with an unknown qualifier code."""
        # Arrange
        qualifier_code = "999"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        # For unknown qualifiers, the result should be None or whatever the parent class returns
        self.assertIsNone(result)

    def test_convert_internal_with_10_Z36_qualifier(self):
        """Test the _convert_internal method with 10 status kategorie code and Z36 status code."""
        # Arrange
        element_components = ["STS", "10", "Z36"]
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
        self.assertIsInstance(result, SegmentSTS)
        self.assertEqual(result.bezeichner, "Grundlage der Energiemenge")
        self.assertEqual(result.statuskategorie.statuskategorie_code, "10")
        self.assertEqual(result.status.status_code, "Z36")

    def test_convert_internal_with_empty_qualifier(self):
        """Test the _convert_internal method with an empty qualifier."""
        # Arrange
        element_components = ["STS", ""]
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
        self.assertIsInstance(result, SegmentSTS)
        self.assertIsNone(result.bezeichner)
        self.assertIsNone(result.statuskategorie)
        self.assertIsNone(result.status)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["STS"]  # Missing required components
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