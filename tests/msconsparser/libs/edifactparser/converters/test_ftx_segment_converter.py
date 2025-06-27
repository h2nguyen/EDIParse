import unittest

from ediparse.libs.edifactparser.converters import FTXSegmentConverter
from ediparse.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.libs.edifactparser.wrappers.segments import SegmentFTX


class TestFTXSegmentConverter(unittest.TestCase):
    """Test case for the FTXSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = FTXSegmentConverter(syntax_parser=self.syntax_parser)
        self.context = APERAKParsingContext()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["FTX", "ABO", "", "", "DE00056266802AO6G56M11SN51G21M24S:201204181115?+00?:303"]

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
        self.assertIsInstance(result, SegmentFTX)
        self.assertEqual(result.textbezug_qualifier, "ABO")
        self.assertEqual(result.text.freier_text_m, "DE00056266802AO6G56M11SN51G21M24S")
        self.assertEqual(result.text.freier_text_c, "201204181115+00:303")

    def test_convert_internal_with_minimal_components(self):
        """Test the _convert_internal method with minimal components."""
        # Arrange
        element_components = ["FTX", "ABO", "", "", "201609160400201609090400?:719"]
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
        self.assertIsInstance(result, SegmentFTX)
        self.assertEqual(result.textbezug_qualifier, "ABO")
        self.assertEqual(result.text.freier_text_m, "201609160400201609090400:719")
        self.assertIsNone(result.text.freier_text_c)


if __name__ == '__main__':
    unittest.main()
