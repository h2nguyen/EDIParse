import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.converters.nad_segment_converter import \
    MSCONSNADSegmentConverter
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentNAD


class TestNADSegmentConverter(unittest.TestCase):
    """Test case for the NADSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = MSCONSNADSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["NAD", "MS", "9920455302123::293"]
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
        self.assertEqual(result.bezeichner, "MP-ID Absender")
        self.assertEqual(result.beteiligter_qualifier, "MS")
        self.assertIsNotNone(result.identifikation_des_beteiligten)
        self.assertEqual(result.identifikation_des_beteiligten.beteiligter_identifikation, "9920455302123")
        self.assertEqual(result.identifikation_des_beteiligten.verantwortliche_stelle_fuer_die_codepflege_code, "293")

    def test_convert_internal_with_mr_qualifier(self):
        """Test the _convert_internal method with MR qualifier."""
        # Arrange
        element_components = ["NAD", "MR", "4012345678901::9"]
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
        self.assertEqual(result.bezeichner, "MP-ID Empfänger")
        self.assertEqual(result.beteiligter_qualifier, "MR")
        self.assertIsNotNone(result.identifikation_des_beteiligten)
        self.assertEqual(result.identifikation_des_beteiligten.beteiligter_identifikation, "4012345678901")
        self.assertEqual(result.identifikation_des_beteiligten.verantwortliche_stelle_fuer_die_codepflege_code, "9")

    def test_convert_internal_with_dp_qualifier(self):
        """Test the _convert_internal method with DP qualifier."""
        # Arrange
        element_components = ["NAD", "DP"]
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
        self.assertEqual(result.beteiligter_qualifier, "DP")
        self.assertIsNone(result.identifikation_des_beteiligten)

    def test_convert_internal_with_unknown_qualifier(self):
        """Test the _convert_internal method with unknown qualifier."""
        # Arrange
        element_components = ["NAD", "XX"]
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
        self.assertIsNone(result.bezeichner)
        self.assertEqual(result.beteiligter_qualifier, "XX")
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
