import unittest

from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.converters.rff_segment_converter import \
    MSCONSRFFSegmentConverter
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentRFF


class TestMSCONSRFFSegmentConverter(unittest.TestCase):
    """Test case for the MSCONSRFFSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = MSCONSRFFSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_initialization(self):
        """Test the initialization of the converter."""
        # Arrange & Act
        converter = MSCONSRFFSegmentConverter(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(converter)
        self.assertEqual(converter._syntax_parser, self.syntax_parser)

    def test_get_identifier_name_with_agi_qualifier(self):
        """Test the _get_identifier_name method with AGI qualifier code."""
        # Arrange
        qualifier_code = "AGI"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Beantragungsnummer")

    def test_get_identifier_name_with_agk_qualifier(self):
        """Test the _get_identifier_name method with AGK qualifier code."""
        # Arrange
        qualifier_code = "AGK"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Anwendungsreferenznummer")

    def test_get_identifier_name_with_mg_qualifier(self):
        """Test the _get_identifier_name method with MG qualifier code."""
        # Arrange
        qualifier_code = "MG"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Gerätenummer")

    def test_get_identifier_name_with_ago_qualifier(self):
        """Test the _get_identifier_name method with AGO qualifier code."""
        # Arrange
        qualifier_code = "AGO"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Absenderreferenz für die Original-Nachricht")
        
    def test_get_identifier_name_with_z13_qualifier(self):
        """Test the _get_identifier_name method with Z13 qualifier code."""
        # Arrange
        qualifier_code = "Z13"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Prüfidentifikator")

    def test_get_identifier_name_with_z30_qualifier(self):
        """Test the _get_identifier_name method with Z30 qualifier code."""
        # Arrange
        qualifier_code = "Z30"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Referenz auf vorherige Stammdatenmeldung des MSB")

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

    def test_convert_internal_with_agi_qualifier(self):
        """Test the _convert_internal method with AGI qualifier code."""
        # Arrange
        element_components = ["RFF", "AGI:12345"]
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
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.bezeichner, "Beantragungsnummer")
        self.assertEqual(result.referenz_qualifier, "AGI")
        self.assertEqual(result.referenz_identifikation, "12345")

    def test_convert_internal_with_ace_qualifier(self):
        """Test the _convert_internal method with ACE qualifier code."""
        # Arrange
        element_components = ["RFF", "ACE:TG9523"]
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
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.referenz_qualifier, "ACE")
        self.assertEqual(result.referenz_identifikation, "TG9523")
        
    def test_convert_internal_with_ago_qualifier(self):
        """Test the _convert_internal method with AGO qualifier code."""
        # Arrange
        element_components = ["RFF", "AGO:12312"]
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
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.referenz_qualifier, "AGO")
        self.assertEqual(result.referenz_identifikation, "12312")
        
    def test_convert_internal_with_tn_qualifier(self):
        """Test the _convert_internal method with TN qualifier code."""
        # Arrange
        element_components = ["RFF", "TN:1"]
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
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.referenz_qualifier, "TN")
        self.assertEqual(result.referenz_identifikation, "1")
        
    def test_convert_internal_with_acw_qualifier(self):
        """Test the _convert_internal method with ACW qualifier code."""
        # Arrange
        element_components = ["RFF", "ACW:9878u7987gh7"]
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
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.referenz_qualifier, "ACW")
        self.assertEqual(result.referenz_identifikation, "9878u7987gh7")
        
    def test_convert_internal_with_ago_qualifier_long_number(self):
        """Test the _convert_internal method with AGO qualifier code and a long number."""
        # Arrange
        element_components = ["RFF", "AGO:798790034532"]
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
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.referenz_qualifier, "AGO")
        self.assertEqual(result.referenz_identifikation, "798790034532")
        
    def test_convert_internal_with_agk_qualifier(self):
        """Test the _convert_internal method with AGK qualifier code."""
        # Arrange
        element_components = ["RFF", "AGK:ABCDE"]
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
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.referenz_qualifier, "AGK")
        self.assertEqual(result.referenz_identifikation, "ABCDE")

    def test_convert_internal_with_minimal_components(self):
        """Test the _convert_internal method with minimal components."""
        # Arrange
        element_components = ["RFF", "MG"]
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
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.referenz_qualifier, "MG")
        self.assertIsNone(result.referenz_identifikation)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["RFF"]  # Missing required components
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