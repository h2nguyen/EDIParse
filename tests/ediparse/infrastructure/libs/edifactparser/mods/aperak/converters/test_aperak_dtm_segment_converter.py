import unittest

from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.aperak.converters.dtm_segment_converter import \
    APERAKDTMSegmentConverter
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentDTM


class TestAPERAKDTMSegmentConverter(unittest.TestCase):
    """Test case for the APERAKDTMSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = APERAKDTMSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = APERAKParsingContext()

    def test_initialization(self):
        """Test the initialization of the converter."""
        # Arrange & Act
        converter = APERAKDTMSegmentConverter(syntax_helper=self.syntax_parser)

        # Assert
        self.assertIsNotNone(converter)
        self.assertEqual(converter._syntax_parser, self.syntax_parser)

    def test_get_identifier_name_with_137_qualifier(self):
        """Test the _get_identifier_name method with 137 qualifier code."""
        # Arrange
        qualifier_code = "137"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Dokumenten-/Nachrichtendatum/-zeit")

    def test_get_identifier_name_with_171_qualifier(self):
        """Test the _get_identifier_name method with 171 qualifier code."""
        # Arrange
        qualifier_code = "171"
        current_segment_group = None

        # Act
        result = self.converter._get_identifier_name(
            qualifier_code=qualifier_code,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertEqual(result, "Referenzdatum/-zeit")

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
        # For unknown qualifiers, the result should be None since neither the child nor parent class handles it
        self.assertIsNone(result)

    def test_convert_internal_with_137_qualifier(self):
        """Test the _convert_internal method with 137 qualifier code."""
        # Arrange
        element_components = ["DTM", "137:202106011315+00:303"]
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
        self.assertIsInstance(result, SegmentDTM)
        self.assertEqual(result.bezeichner, "Dokumenten-/Nachrichtendatum/-zeit")
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "137")
        self.assertEqual(result.datum_oder_uhrzeit_oder_zeitspanne_wert, "202106011315+00")
        self.assertEqual(result.datums_oder_uhrzeit_oder_zeitspannen_format_code, "303")

    def test_convert_internal_with_171_qualifier(self):
        """Test the _convert_internal method with 171 qualifier code."""
        # Arrange
        element_components = ["DTM", "171:202106011315+00:303"]
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
        self.assertIsInstance(result, SegmentDTM)
        self.assertEqual(result.bezeichner, "Referenzdatum/-zeit")
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "171")
        self.assertEqual(result.datum_oder_uhrzeit_oder_zeitspanne_wert, "202106011315+00")
        self.assertEqual(result.datums_oder_uhrzeit_oder_zeitspannen_format_code, "303")

    def test_convert_internal_with_minimal_components(self):
        """Test the _convert_internal method with minimal components."""
        # Arrange
        element_components = ["DTM", "137"]
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
        self.assertIsInstance(result, SegmentDTM)
        self.assertEqual(result.bezeichner, "Dokumenten-/Nachrichtendatum/-zeit")
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "137")
        self.assertIsNone(result.datum_oder_uhrzeit_oder_zeitspanne_wert)
        self.assertIsNone(result.datums_oder_uhrzeit_oder_zeitspannen_format_code)

    def test_convert_internal_with_empty_qualifier(self):
        """Test the _convert_internal method with an empty qualifier."""
        # Arrange
        element_components = ["DTM", ""]
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
        self.assertIsInstance(result, SegmentDTM)
        self.assertIsNone(result.bezeichner)
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "")
        self.assertIsNone(result.datum_oder_uhrzeit_oder_zeitspanne_wert)
        self.assertIsNone(result.datums_oder_uhrzeit_oder_zeitspannen_format_code)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["DTM"]  # Missing required components
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
