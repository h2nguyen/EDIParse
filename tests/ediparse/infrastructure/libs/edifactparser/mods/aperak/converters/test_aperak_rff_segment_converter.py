import unittest

from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.aperak.converters.rff_segment_converter import \
    APERAKRFFSegmentConverter
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentRFF


class TestAPERAKRFFSegmentConverter(unittest.TestCase):
    """Test case for the APERAKRFFSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = APERAKRFFSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = APERAKParsingContext()

    def test_initialization(self):
        """Test the initialization of the converter."""
        # Arrange & Act
        converter = APERAKRFFSegmentConverter(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(converter)
        self.assertEqual(converter._syntax_parser, self.syntax_parser)

    def test_get_identifier_name_with_ace_qualifier(self):
        """Test the _get_identifier_name method with ACE qualifier code."""
        # Arrange
        qualifier_code = "ACE"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Nummer des zugehörigen Dokuments")

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

    def test_get_identifier_name_with_tn_qualifier(self):
        """Test the _get_identifier_name method with TN qualifier code."""
        # Arrange
        qualifier_code = "TN"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Transaktions-Referenznummer")

    def test_get_identifier_name_with_z02_qualifier(self):
        """Test the _get_identifier_name method with Z02 qualifier code."""
        # Arrange
        qualifier_code = "Z02"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Ortsangabe des AHB-Fehlers")

    def test_get_identifier_name_with_z08_qualifier(self):
        """Test the _get_identifier_name method with Z08 qualifier code."""
        # Arrange
        qualifier_code = "Z08"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "MP-ID des nachfolgenden Netzbetreibers")

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
        # For unknown qualifiers, the result should be None since neither the child nor parent class handles it
        self.assertIsNone(result)

    def test_convert_internal_with_ace_qualifier(self):
        """Test the _convert_internal method with ACE qualifier code."""
        # Arrange
        element_components = ["RFF", "ACE:12345"]
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
        self.assertEqual(result.bezeichner, "Nummer des zugehörigen Dokuments")
        self.assertEqual(result.referenz_qualifier, "ACE")
        self.assertEqual(result.referenz_identifikation, "12345")

    def test_convert_internal_with_ago_qualifier(self):
        """Test the _convert_internal method with AGO qualifier code."""
        # Arrange
        element_components = ["RFF", "AGO:67890"]
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
        self.assertEqual(result.bezeichner, "Absenderreferenz für die Original-Nachricht")
        self.assertEqual(result.referenz_qualifier, "AGO")
        self.assertEqual(result.referenz_identifikation, "67890")

    def test_convert_internal_with_minimal_components(self):
        """Test the _convert_internal method with minimal components."""
        # Arrange
        element_components = ["RFF", "TN:"]
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
        self.assertEqual(result.bezeichner, "Transaktions-Referenznummer")
        self.assertEqual(result.referenz_qualifier, "TN")
        self.assertEqual(result.referenz_identifikation, "")

    def test_convert_internal_with_empty_qualifier(self):
        """Test the _convert_internal method with an empty qualifier."""
        # Arrange
        element_components = ["RFF", ":"]
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
        self.assertIsNone(result.bezeichner)
        self.assertEqual(result.referenz_qualifier, "")
        self.assertEqual(result.referenz_identifikation, "")

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
