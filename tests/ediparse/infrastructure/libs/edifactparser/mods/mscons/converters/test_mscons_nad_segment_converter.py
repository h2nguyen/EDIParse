import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.converters.nad_segment_converter import \
    MSCONSNADSegmentConverter
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentNAD


class TestMSCONSNADSegmentConverter(unittest.TestCase):
    """Test case for the MSCONSNADSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = MSCONSNADSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_initialization(self):
        """Test the initialization of the converter."""
        # Arrange & Act
        converter = MSCONSNADSegmentConverter(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(converter)
        self.assertEqual(converter._syntax_parser, self.syntax_parser)

    def test_get_identifier_name_with_dp_qualifier(self):
        """Test the _get_identifier_name method with DP qualifier code."""
        # Arrange
        qualifier_code = "DP"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Name und Adresse")

    def test_get_identifier_name_with_ded_qualifier(self):
        """Test the _get_identifier_name method with DED qualifier code."""
        # Arrange
        qualifier_code = "DED"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Name und Adresse")

    def test_get_identifier_name_with_z15_qualifier(self):
        """Test the _get_identifier_name method with Z15 qualifier code."""
        # Arrange
        qualifier_code = "Z15"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Name und Adresse")

    def test_get_identifier_name_with_mr_qualifier(self):
        """Test the _get_identifier_name method with MR qualifier code (handled by parent class)."""
        # Arrange
        qualifier_code = "MR"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "MP-ID Empfänger")

    def test_get_identifier_name_with_ms_qualifier(self):
        """Test the _get_identifier_name method with MS qualifier code (handled by parent class)."""
        # Arrange
        qualifier_code = "MS"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "MP-ID Absender")

    def test_get_identifier_name_with_unknown_qualifier(self):
        """Test the _get_identifier_name method with an unknown qualifier code."""
        # Arrange
        qualifier_code = "XXX"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        # For unknown qualifiers, the result should be None
        self.assertIsNone(result)

    def test_convert_internal_with_ded_qualifier(self):
        """Test the _convert_internal method with DED qualifier code."""
        # Arrange
        element_components = ["NAD", "DED", "9900204000003::293"]
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
        self.assertIsInstance(result, SegmentNAD)
        self.assertEqual(result.bezeichner, "Name und Adresse")
        self.assertEqual(result.beteiligter_qualifier, "DED")
        self.assertIsNotNone(result.identifikation_des_beteiligten)
        self.assertEqual(result.identifikation_des_beteiligten.beteiligter_identifikation, "9900204000003")
        self.assertEqual(result.identifikation_des_beteiligten.verantwortliche_stelle_fuer_die_codepflege_code, "293")

    def test_convert_internal_with_z15_qualifier(self):
        """Test the _convert_internal method with Z15 qualifier code."""
        # Arrange
        element_components = ["NAD", "Z15", "9900204000004::293"]
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
        self.assertIsInstance(result, SegmentNAD)
        self.assertEqual(result.bezeichner, "Name und Adresse")
        self.assertEqual(result.beteiligter_qualifier, "Z15")
        self.assertIsNotNone(result.identifikation_des_beteiligten)
        self.assertEqual(result.identifikation_des_beteiligten.beteiligter_identifikation, "9900204000004")
        self.assertEqual(result.identifikation_des_beteiligten.verantwortliche_stelle_fuer_die_codepflege_code, "293")

    def test_convert_internal_with_minimal_components(self):
        """Test the _convert_internal method with minimal components."""
        # Arrange
        element_components = ["NAD", "DED"]
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
        self.assertIsInstance(result, SegmentNAD)
        self.assertEqual(result.bezeichner, "Name und Adresse")
        self.assertEqual(result.beteiligter_qualifier, "DED")
        self.assertIsNone(result.identifikation_des_beteiligten)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["NAD"]  # Missing required components
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