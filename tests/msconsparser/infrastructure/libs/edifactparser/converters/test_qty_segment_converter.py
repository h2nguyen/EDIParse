import unittest

from ediparse.infrastructure.libs.edifactparser.converters.qty_segment_converter import QTYSegmentConverter
from ediparse.infrastructure.libs.edifactparser.utils import EdifactSyntaxHelper
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext
from ediparse.infrastructure.libs.edifactparser.wrappers.segments.message_structure import EdifactInterchange, SegmentUNA
from ediparse.infrastructure.libs.edifactparser.wrappers.segments.measurement import SegmentQTY


class TestQTYSegmentConverter(unittest.TestCase):
    """Test case for the QTYSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = QTYSegmentConverter(syntax_parser=self.syntax_parser)
        self.context = MSCONSParsingContext()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["QTY", "220:4250.465:D54"]
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
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "220")
        self.assertEqual(result.menge, 4250.465)
        self.assertEqual(result.masseinheit_code, "D54")

    def test_convert_internal_without_masseinheit_code(self):
        """Test the _convert_internal method without masseinheit_code."""
        # Arrange
        element_components = ["QTY", "67:4250.465"]
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
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "67")
        self.assertEqual(result.menge, 4250.465)
        self.assertIsNone(result.masseinheit_code)

    def test_convert_internal_with_decimal_places(self):
        """Test the _convert_internal method with decimal places."""
        # Arrange
        element_components = ["QTY", "220:4.123:D54"]
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
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "220")
        self.assertEqual(result.menge, 4.123)
        self.assertEqual(result.masseinheit_code, "D54")

    def test_convert_internal_with_negative_value(self):
        """Test the _convert_internal method with negative value."""
        # Arrange
        element_components = ["QTY", "79:-4.987:KWH"]
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
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "79")
        self.assertEqual(result.menge, -4.987)
        self.assertEqual(result.masseinheit_code, "KWH")

    def test_convert_with_exception_missing_components(self):
        """Test the convert method with an exception due to missing components."""
        # Arrange
        line_number = 1
        element_components = ["QTY"]  # Missing required components
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

    def test_convert_with_exception_invalid_menge(self):
        """Test the convert method with an exception due to invalid menge."""
        # Arrange
        line_number = 1
        element_components = ["QTY", "220:invalid:D54"]  # Invalid menge
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

    def test_convert_internal_with_custom_decimal_mark(self):
        """Test the _convert_internal method with a custom decimal mark in UNA."""
        # Arrange
        element_components = ["QTY", "220:4250,465:D54"]  # Note the comma as decimal mark
        last_segment_type = None
        current_segment_group = None

        # Create a context with a custom decimal mark
        context = MSCONSParsingContext()
        context.interchange = EdifactInterchange()
        context.interchange.una_service_string_advice = SegmentUNA(
            component_separator=":",
            element_separator="+",
            decimal_mark=",",  # Comma as decimal mark
            release_character="?",
            reserved=" ",
            segment_terminator="'"
        )

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=context
        )

        # Assert
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "220")
        self.assertEqual(result.menge, 4250.465)  # Should be converted to float correctly
        self.assertEqual(result.masseinheit_code, "D54")

    def test_convert_internal_with_missing_una(self):
        """Test the _convert_internal method when UNA service string advice is missing."""
        # Arrange
        element_components = ["QTY", "220:4250.465:D54"]  # Note the dot as decimal mark
        last_segment_type = None
        current_segment_group = None

        # Create a context without UNA service string advice
        context = MSCONSParsingContext()
        # Explicitly set to None to simulate missing UNA
        context.interchange.una_service_string_advice = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=context
        )

        # Assert
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "220")
        self.assertEqual(result.menge, 4250.465)  # Should use default dot as decimal mark
        self.assertEqual(result.masseinheit_code, "D54")

    def test_convert_internal_with_empty_decimal_mark(self):
        """Test the _convert_internal method when decimal mark in UNA is empty."""
        # Arrange
        element_components = ["QTY", "220:4250.465:D54"]  # Note the dot as decimal mark
        last_segment_type = None
        current_segment_group = None

        # Create a context with empty decimal mark
        context = MSCONSParsingContext()
        context.interchange = EdifactInterchange()
        context.interchange.una_service_string_advice = SegmentUNA(
            component_separator=":",
            element_separator="+",
            decimal_mark="",  # Empty decimal mark
            release_character="?",
            reserved=" ",
            segment_terminator="'"
        )

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=context
        )

        # Assert
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "220")
        self.assertEqual(result.menge, 4250.465)  # Should use default dot as decimal mark
        self.assertEqual(result.masseinheit_code, "D54")

    def test_convert_internal_with_decimal_mark_replacement(self):
        """Test the _convert_internal method with decimal mark replacement."""
        # Arrange
        element_components = ["QTY", "220:4250.465:D54"]  # Note the dot as decimal mark in string
        last_segment_type = None
        current_segment_group = None

        # Create a context with comma as decimal mark
        context = MSCONSParsingContext()
        context.interchange = EdifactInterchange()
        context.interchange.una_service_string_advice = SegmentUNA(
            component_separator=":",
            element_separator="+",
            decimal_mark=",",  # Comma as decimal mark in UNA
            release_character="?",
            reserved=" ",
            segment_terminator="'"
        )

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=context
        )

        # Assert
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "220")
        self.assertEqual(result.menge, 4250.465)  # Should be converted to float correctly
        self.assertEqual(result.masseinheit_code, "D54")


if __name__ == '__main__':
    unittest.main()
