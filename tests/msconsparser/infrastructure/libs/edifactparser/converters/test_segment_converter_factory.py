import unittest

from ediparse.infrastructure.libs.edifactparser.converters.segment_converter_factory import SegmentConverterFactory
from ediparse.infrastructure.libs.edifactparser.mods.module_constants import EdifactMessageType
from ediparse.infrastructure.libs.edifactparser.utils.edifact_syntax_helper import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.wrappers.context import InitialParsingContext


class TestSegmentConverterFactory(unittest.TestCase):
    def setUp(self):
        self.syntax_parser = EdifactSyntaxHelper()
        self.factory = SegmentConverterFactory(self.syntax_parser)

    def test_get_converter_with_base_converter(self):
        """Test that get_converter returns the base converter when no message-specific converters are found."""
        # Choose a segment type that likely has a base converter but no message-specific converters
        segment_type = "UNA"  # Adjust this if needed
        converter = self.factory.get_converter(segment_type)
        self.assertIsNotNone(converter, f"No converter found for segment type {segment_type}")

    def test_get_converter_with_message_specific_converter(self):
        """Test that get_converter returns the message-specific converter when available."""
        # Choose a segment type that likely has message-specific converters
        segment_type = "DTM"  # Adjust this if needed
        context = InitialParsingContext()
        context.message_type = EdifactMessageType.APERAK
        converter = self.factory.get_converter(segment_type, context)
        self.assertIsNotNone(converter, f"No converter found for segment type {segment_type} and message type {context.message_type}")

    def test_get_converter_fallback_to_base(self):
        """Test that get_converter falls back to the base converter when no message-specific converter is found."""
        # Choose a segment type that likely has a base converter and message-specific converters for some message types
        segment_type = "DTM"  # Adjust this if needed
        context = InitialParsingContext()
        context.message_type = EdifactMessageType.MSCONS  # Assuming this message type doesn't have a specific converter for DTM
        converter = self.factory.get_converter(segment_type, context)
        self.assertIsNotNone(converter, f"No converter found for segment type {segment_type} and message type {context.message_type}")


if __name__ == '__main__':
    unittest.main()
