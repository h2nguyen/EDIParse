"""
Tests for the ParsingContextFactory class.

This module contains tests for the ParsingContextFactory class, which is responsible
for creating instances of ParsingContext subclasses based on the EDIFACT message type.
"""
import unittest

from ediparse.infrastructure.libs.edifactparser.exceptions import EdifactParserException
from ediparse.infrastructure.libs.edifactparser.utils import ParsingContextFactory
from ediparse.infrastructure.libs.edifactparser.mods.aperak.context import APERAKParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.module_constants import EdifactMessageType
from ediparse.infrastructure.libs.edifactparser.wrappers.context import InitialParsingContext
from ediparse.infrastructure.libs.edifactparser.mods.mscons.context import MSCONSParsingContext


class TestParsingContextFactory(unittest.TestCase):
    """Test cases for the ParsingContextFactory class."""

    def setUp(self):
        """Set up the test case."""
        # Initialize a default parsing context for tests
        self.default_context = InitialParsingContext()

    def tearDown(self):
        """Clean up after the test case."""
        # No cleanup needed for these tests
        pass

    def test_create_context_mscons(self):
        """Test creating a context for MSCONS message type."""
        # Arrange
        message_type = EdifactMessageType.MSCONS

        # Act
        context = ParsingContextFactory.create_context(message_type)

        # Assert
        self.assertIsInstance(context, MSCONSParsingContext)
        self.assertEqual(context.message_type, EdifactMessageType.MSCONS)

    def test_create_context_aperak(self):
        """Test creating a context for APERAK message type."""
        # Arrange
        message_type = EdifactMessageType.APERAK

        # Act
        context = ParsingContextFactory.create_context(message_type)

        # Assert
        self.assertIsInstance(context, APERAKParsingContext)
        self.assertEqual(context.message_type, EdifactMessageType.APERAK)

    def test_create_context_unsupported(self):
        """Test creating a context for an unsupported message type."""
        # Arrange
        mock_type = "UNSUPPORTED"  # Create a mock EdifactMessageType that's not supported

        # Act & Assert
        with self.assertRaises(EdifactParserException) as context:
            ParsingContextFactory.create_context(mock_type)
        self.assertIn("Unsupported message type", str(context.exception))

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
        context = ParsingContextFactory.identify_and_create_context(edifact_text, self.default_context)

        # Assert
        self.assertIsInstance(context, MSCONSParsingContext)
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
        context = ParsingContextFactory.identify_and_create_context(edifact_text, self.default_context)

        # Assert
        self.assertIsInstance(context, APERAKParsingContext)
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

        # Act & Assert
        with self.assertRaises(EdifactParserException) as context:
            ParsingContextFactory.identify_and_create_context(edifact_text, self.default_context)
        self.assertEqual("No valid message type found in the EDIFACT message.", str(context.exception))

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

        # Act & Assert
        for string_content, message_type_value, expected_result in test_cases:
            result = ParsingContextFactory._find_message_type(
                string_content, 
                message_type_value, 
                self.default_context
            )
            self.assertEqual(
                result, 
                expected_result, 
                f"Failed for string_content='{string_content}', message_type_value='{message_type_value}'"
            )


if __name__ == "__main__":
    unittest.main()
