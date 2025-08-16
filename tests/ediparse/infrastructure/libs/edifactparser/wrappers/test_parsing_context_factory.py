"""
Tests for the ParsingContextFactory class.

This module contains tests for the ParsingContextFactory class, which is responsible
for creating instances of ParsingContext subclasses based on the EDIFACT message type.
"""
import unittest

from ediparse.infrastructure.libs.edifactparser.exceptions import EdifactParserException
from ediparse.infrastructure.libs.edifactparser.mods.module_constants import EdifactMessageType
from ediparse.infrastructure.libs.edifactparser.wrappers.context import InitialParsingContext
from ediparse.infrastructure.libs.edifactparser.wrappers.context_factory import ParsingContextFactory


class TestParsingContextFactory(unittest.TestCase):
    """Test cases for the ParsingContextFactory class."""

    def setUp(self):
        """Set up the test case."""
        # Initialize a default parsing context for tests
        self.default_context = InitialParsingContext()
        # Initialize the factory
        self.factory = ParsingContextFactory()

    def tearDown(self):
        """Clean up after the test case."""
        # No cleanup needed for these tests
        pass

    def test_create_context_mscons(self):
        """Test creating a context for MSCONS message type."""
        # Arrange
        message_type = EdifactMessageType.MSCONS

        # Act
        context = self.factory.create_context(message_type)

        # Verify
        self.assertIsNotNone(context)
        self.assertEqual(context.message_type, EdifactMessageType.MSCONS)

    def test_create_context_aperak(self):
        """Test creating a context for APERAK message type."""
        # Arrange
        message_type = EdifactMessageType.APERAK

        # Act
        context = self.factory.create_context(message_type)

        # Verify
        self.assertIsNotNone(context)
        self.assertEqual(context.message_type, EdifactMessageType.APERAK)

    def test_create_context_unsupported(self):
        """Test creating a context for an unsupported message type."""
        # Arrange
        mock_type = "UNSUPPORTED"  # Create a mock EdifactMessageType that's not supported

        # Act & Verify
        with self.assertRaises(EdifactParserException) as ctx:
            self.factory.create_context(mock_type)
        self.assertIn("Unsupported message type", str(ctx.exception))

    def test_identify_and_create_context_mscons(self):
        """Test identifying and creating a context for MSCONS message."""
        # Arrange
        edifact_text = """
UNA:+.? '
UNB+UNOC:3+4012345678901:14+4012345678901:14+200426:1151+ABC4711++TL++++1'
UNH+1+MSCONS:D:04B:UN:2.4c+UNB_DE0020_nr_1+1:C'
BGM+7+MSI5422+9'
DTM+137:202106011315?+00:303'
RFF+AGI:AFN9523'
DTM+293:20210601060030?+00:304'
RFF+Z30:UTILMDXYZ_1235'
RFF+Z13:13002'        
        """

        # Act
        context = self.factory.identify_and_create_context(edifact_text, self.default_context)

        # Verify
        self.assertIsNotNone(context)
        self.assertEqual(context.message_type, EdifactMessageType.MSCONS)

    def test_identify_and_create_context_aperak(self):
        """Test identifying and creating a context for APERAK message."""
        # Arrange
        edifact_text = """
UNB+UNOC:3+9900204000002:500+4012345000023:500+210408:1010+121234567ABC7D'
UNH+1234EF66EF3QAJ+APERAK:D:07B:UN:2.1i'
BGM+313+AFBM5422'
DTM+137:202104081015?+00:303'
RFF+ACE:TG9523'
        """

        # Act
        context = self.factory.identify_and_create_context(edifact_text, self.default_context)

        # Verify
        self.assertIsNotNone(context)
        self.assertEqual(context.message_type, EdifactMessageType.APERAK)

    def test_identify_and_create_context_no_match(self):
        """Test identifying and creating a context when no message type is found."""
        # Arrange
        edifact_text = """
UNA:+.? '
UNB+UNOC:3+4012345678901:14+4012345678901:14+200426:1151+ABC4711++TL++++1'
UNH+1+MSCONSAPERAK:D:04B:UN:2.4c+UNB_DE0020_nr_1+1:C'
BGM+7+MSI5422+9'
DTM+137:202106011315?+00:303'
RFF+AGI:AFN9523'
DTM+293:20210601060030?+00:304'
RFF+Z30:UTILMDXYZ_1235'
RFF+Z13:13002'        
        """

        # Act & Verify
        with self.assertRaises(EdifactParserException) as ctx:
            self.factory.identify_and_create_context(edifact_text, self.default_context)
        self.assertEqual("No valid message type found in the EDIFACT message.", str(ctx.exception))

    def test_identify_and_create_context_with_custom_delimiters_in_context(self):
        """Identify message type using delimiters provided by parsing context (UNA)."""
        # Arrange
        # Prepare a dummy UNA-like object directly on the default context to avoid heavy imports
        from types import SimpleNamespace

        self.default_context.interchange.una_service_string_advice = SimpleNamespace(
            component_separator="/",
            element_separator=";",
            decimal_mark=",",
            release_character="?",
            reserved=" ",
            segment_terminator="'",
        )
        # EDIFACT text uses the custom separators
        edifact_text = "UNH;1;MSCONS/D/04B/UN/2.4c;X'\nBGM;7;MSI5422;9'"

        # Act
        result_context = self.factory.identify_and_create_context(edifact_text, self.default_context)

        # Verify
        self.assertIsNotNone(result_context)
        self.assertEqual(result_context.message_type, EdifactMessageType.MSCONS)

    def test_identify_and_create_context_case_insensitive_token(self):
        """Identify message type when UNH token uses lowercase (case-insensitive)."""
        # Arrange
        edifact_text = "UNH+1+mscons:D:04B:UN:2.4c'"

        # Act
        context = self.factory.identify_and_create_context(edifact_text, self.default_context)

        # Verify
        self.assertIsNotNone(context)
        self.assertEqual(context.message_type, EdifactMessageType.MSCONS)

    def test_identify_and_create_context_multiple_types_prefers_enum_order(self):
        """When multiple types are present, prefer the first in EdifactMessageType enum (APERAK)."""
        # Arrange
        edifact_text = """
UNH+1+APERAK:D:07B:UN:2.1i'
UNH+2+MSCONS:D:04B:UN:2.4c'
        """
        # Sanity check: enum order should be APERAK first
        self.assertEqual(list(EdifactMessageType)[0], EdifactMessageType.APERAK)

        # Act
        context = self.factory.identify_and_create_context(edifact_text, self.default_context)

        # Verify
        self.assertIsNotNone(context)
        self.assertEqual(context.message_type, EdifactMessageType.APERAK)

    def test_identify_and_create_context_with_empty_text_raises(self):
        """Empty EDIFACT text should raise EdifactParserException (no type found)."""
        # Arrange
        edifact_text = ""

        # Act & Verify
        with self.assertRaises(EdifactParserException) as ctx:
            self.factory.identify_and_create_context(edifact_text, self.default_context)
        self.assertIn("No valid message type found", str(ctx.exception))

    def test_find_message_type(self):
        """Test the _find_message_type method."""
        # Arrange
        test_cases = [
            # (string_content, message_type_value, expected_result)
            ("+MSCONS:", "MSCONS", True),  # Exact match
            ("+mscons:", "MSCONS", True),  # Case-insensitive match (lowercase string)
            ("+MSCONS:", "mscons", True),  # Case-insensitive match (lowercase message type)
            ("This is a +MSCONS: message", "MSCONS", True),  # Message type as part of larger text
            ("This is a test", "MSCONS", False),  # No match
        ]

        # Act & Verify
        for string_content, message_type_value, expected_result in test_cases:
            result = self.factory._find_message_type(
                string_content,
                message_type_value,
                self.default_context,
            )
            self.assertEqual(
                result,
                expected_result,
                f"Failed for string_content='{string_content}', message_type_value='{message_type_value}'",
            )

    def test_find_message_type_uses_defaults_when_context_none(self):
        """_find_message_type should fall back to default separators if context is None."""
        # Arrange
        string_content = "+MSCONS:"
        # Act
        result = self.factory._find_message_type(string_content, "MSCONS", None)
        # Verify
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
