import unittest

from ediparse.infrastructure.libs.edifactparser.converters.com_segment_converter import COMSegmentConverter
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentCOM


class TestCOMSegmentConverter(unittest.TestCase):
    """Test case for the COMSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = COMSegmentConverter(syntax_parser=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["COM", "?+493991185138:TE"]
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
        self.assertIsInstance(result, SegmentCOM)
        self.assertIsNotNone(result.kommunikationsverbindung)
        self.assertEqual(result.kommunikationsverbindung.kommunikationsadresse_identifikation, "+493991185138")
        self.assertEqual(result.kommunikationsverbindung.kommunikationsadresse_qualifier, "TE")

    def test_convert_internal_without_qualifier(self):
        """Test the _convert_internal method without qualifier."""
        # Arrange
        element_components = ["COM", "email@example.com"]
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
        self.assertIsInstance(result, SegmentCOM)
        self.assertIsNotNone(result.kommunikationsverbindung)
        self.assertEqual(result.kommunikationsverbindung.kommunikationsadresse_identifikation, "email@example.com")
        self.assertIsNone(result.kommunikationsverbindung.kommunikationsadresse_qualifier)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["COM"]  # Missing required components
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
