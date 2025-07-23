import unittest

from ediparse.infrastructure.libs.edifactparser.converters.loc_segment_converter import LOCSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentLOC


class TestLOCSegmentConverter(unittest.TestCase):
    """Test case for the LOCSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = LOCSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["LOC", "237", "11XUENBSOLS----X", "11XVNBSOLS-----X"]
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
        self.assertIsInstance(result, SegmentLOC)
        self.assertEqual(result.ortsangabe_qualifier, "237")
        self.assertIsNotNone(result.ortsangabe)
        self.assertEqual(result.ortsangabe.ortsangabe_code, "11XUENBSOLS----X")
        self.assertIsNotNone(result.zugehoeriger_ort_1_identifikation)
        self.assertEqual(result.zugehoeriger_ort_1_identifikation.erster_zugehoeriger_platz_ort_code,
                         "11XVNBSOLS-----X")

    def test_convert_internal_with_only_ortsangabe(self):
        """Test the _convert_internal method with only ortsangabe."""
        # Arrange
        element_components = ["LOC", "107", "11YR000000011247"]
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
        self.assertIsInstance(result, SegmentLOC)
        self.assertEqual(result.ortsangabe_qualifier, "107")
        self.assertIsNotNone(result.ortsangabe)
        self.assertEqual(result.ortsangabe.ortsangabe_code, "11YR000000011247")
        self.assertIsNone(result.zugehoeriger_ort_1_identifikation)

    def test_convert_internal_with_minimal_components(self):
        """Test the _convert_internal method with minimal components."""
        # Arrange
        element_components = ["LOC", "Z04"]
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
        self.assertIsInstance(result, SegmentLOC)
        self.assertEqual(result.ortsangabe_qualifier, "Z04")
        self.assertIsNone(result.ortsangabe)
        self.assertIsNone(result.zugehoeriger_ort_1_identifikation)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["LOC"]  # Missing required components
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
