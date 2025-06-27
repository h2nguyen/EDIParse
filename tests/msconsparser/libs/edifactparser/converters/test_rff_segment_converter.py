import unittest

from ediparse.libs.edifactparser.converters import RFFSegmentConverter
from ediparse.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.libs.edifactparser.wrappers.segments import SegmentRFF


class TestRFFSegmentConverter(unittest.TestCase):
    """Test case for the RFFSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.context = MSCONSParsingContext()
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = RFFSegmentConverter(syntax_parser=self.syntax_parser)

    def test_convert_internal_with_agi_qualifier(self):
        """Test the _convert_internal method with AGI qualifier."""
        # Arrange
        element_components = ["RFF", "AGI:AFN9523"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=MSCONSParsingContext()
        )

        # Assert
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.bezeichner, "Referenzangaben")
        self.assertEqual(result.referenz_qualifier, "AGI")
        self.assertEqual(result.referenz_identifikation, "AFN9523")

    def test_convert_internal_with_agk_qualifier(self):
        """Test the _convert_internal method with AGK qualifier."""
        # Arrange
        element_components = ["RFF", "AGK:12345"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=MSCONSParsingContext()
        )

        # Assert
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.bezeichner, "Konfigurations-ID")
        self.assertEqual(result.referenz_qualifier, "AGK")
        self.assertEqual(result.referenz_identifikation, "12345")

    def test_convert_internal_with_mg_qualifier(self):
        """Test the _convert_internal method with MG qualifier."""
        # Arrange
        element_components = ["RFF", "MG:67890"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=MSCONSParsingContext()
        )

        # Assert
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.bezeichner, "Gerätenummer")
        self.assertEqual(result.referenz_qualifier, "MG")
        self.assertEqual(result.referenz_identifikation, "67890")

    def test_convert_internal_with_z13_qualifier(self):
        """Test the _convert_internal method with Z13 qualifier."""
        # Arrange
        element_components = ["RFF", "Z13:13025"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=MSCONSParsingContext()
        )

        # Assert
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.bezeichner, "Prüfidentifikator")
        self.assertEqual(result.referenz_qualifier, "Z13")
        self.assertEqual(result.referenz_identifikation, "13025")

    def test_convert_internal_with_z30_qualifier(self):
        """Test the _convert_internal method with Z30 qualifier."""
        # Arrange
        element_components = ["RFF", "Z30:MSB12345"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=MSCONSParsingContext()
        )

        # Assert
        self.assertIsInstance(result, SegmentRFF)
        self.assertEqual(result.bezeichner, "Referenz auf vorherige Stammdatenmeldung des MSB")
        self.assertEqual(result.referenz_qualifier, "Z30")
        self.assertEqual(result.referenz_identifikation, "MSB12345")

    def test_convert_internal_with_unknown_qualifier(self):
        """Test the _convert_internal method with unknown qualifier."""
        # Arrange
        element_components = ["RFF", "XX:12345"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=MSCONSParsingContext()
        )

        # Assert
        self.assertIsInstance(result, SegmentRFF)
        self.assertIsNone(result.bezeichner)
        self.assertEqual(result.referenz_qualifier, "XX")
        self.assertEqual(result.referenz_identifikation, "12345")

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
                context=MSCONSParsingContext()
            )


if __name__ == '__main__':
    unittest.main()
