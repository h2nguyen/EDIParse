import unittest

from ediparse.infrastructure.libs.edifactparser.converters.erc_segment_converter import ERCSegmentConverter
from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.segments import SegmentERC


class TestERCSegmentConverter(unittest.TestCase):
    """Test case for the ERCSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = ERCSegmentConverter(syntax_helper=self.syntax_parser)
        self.context = APERAKParsingContext()

    def test_convert_internal(self):
        """Test the _convert_internal method."""
        # Arrange
        element_components = ["ERC", "Z10"]
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
        self.assertIsInstance(result, SegmentERC)
        self.assertEqual(result.fehlercode.anwendungsfehler_code, "Z10")


if __name__ == '__main__':
    unittest.main()
