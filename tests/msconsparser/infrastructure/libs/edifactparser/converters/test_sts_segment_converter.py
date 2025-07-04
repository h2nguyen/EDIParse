import unittest

from ediparse.infrastructure.libs.edifactparser.converters.sts_segment_converter import STSSegmentConverter
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentSTS


class TestSTSSegmentConverter(unittest.TestCase):
    """Test case for the STSSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.context = MSCONSParsingContext()
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = STSSegmentConverter(syntax_parser=self.syntax_parser)

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["STS", "Z34", "", "Z81"]
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
        self.assertEqual(result.bezeichner, "Korrekturgrund")
        self.assertIsNotNone(result.statuskategorie)
        self.assertEqual(result.statuskategorie.statuskategorie_code, "Z34")
        self.assertIsNone(result.status)
        self.assertIsNotNone(result.statusanlass)
        self.assertEqual(result.statusanlass.statusanlass_code, "Z81")

    def test_convert_internal_with_z40_qualifier(self):
        """Test the _convert_internal method with Z40 qualifier."""
        # Arrange
        element_components = ["STS", "Z40", "", "Z74"]
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
        self.assertEqual(result.bezeichner, "Grund der Ersatzwertbildung")
        self.assertIsNotNone(result.statuskategorie)
        self.assertEqual(result.statuskategorie.statuskategorie_code, "Z40")
        self.assertIsNone(result.status)
        self.assertIsNotNone(result.statusanlass)
        self.assertEqual(result.statusanlass.statusanlass_code, "Z74")

    def test_convert_internal_with_10_qualifier(self):
        """Test the _convert_internal method with 10 qualifier."""
        # Arrange
        element_components = ["STS", "10", "E01", ""]
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
        self.assertIsNotNone(result.statuskategorie)
        self.assertEqual(result.statuskategorie.statuskategorie_code, "10")
        self.assertIsNotNone(result.status)
        self.assertEqual(result.status.status_code, "E01")
        self.assertIsNone(result.statusanlass)

    def test_convert_internal_with_z31_qualifier(self):
        """Test the _convert_internal method with Z31 qualifier."""
        # Arrange
        element_components = ["STS", "Z31"]
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
        self.assertEqual(result.bezeichner, "Gasqualität")
        self.assertIsNotNone(result.statuskategorie)
        self.assertEqual(result.statuskategorie.statuskategorie_code, "Z31")
        self.assertIsNone(result.status)
        self.assertIsNone(result.statusanlass)

    def test_convert_internal_with_z32_qualifier(self):
        """Test the _convert_internal method with Z32 qualifier."""
        # Arrange
        element_components = ["STS", "Z32"]
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
        self.assertEqual(result.bezeichner, "Ersatzwertbildungsverfahren")
        self.assertIsNotNone(result.statuskategorie)
        self.assertEqual(result.statuskategorie.statuskategorie_code, "Z32")
        self.assertIsNone(result.status)
        self.assertIsNone(result.statusanlass)

    def test_convert_internal_with_z33_qualifier(self):
        """Test the _convert_internal method with Z33 qualifier."""
        # Arrange
        element_components = ["STS", "Z33"]
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
        self.assertEqual(result.bezeichner, "Plausibilisierungshinweis")
        self.assertIsNotNone(result.statuskategorie)
        self.assertEqual(result.statuskategorie.statuskategorie_code, "Z33")
        self.assertIsNone(result.status)
        self.assertIsNone(result.statusanlass)

    def test_convert_internal_with_unknown_qualifier(self):
        """Test the _convert_internal method with unknown qualifier."""
        # Arrange
        element_components = ["STS", "XX"]
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
        self.assertIsNotNone(result.statuskategorie)
        self.assertEqual(result.statuskategorie.statuskategorie_code, "XX")
        self.assertIsNone(result.status)
        self.assertIsNone(result.statusanlass)

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
