import os
import unittest
import json
from pathlib import Path

from ediparse.infrastructure.libs.edifactparser.exceptions import EdifactParserException
from ediparse.infrastructure.libs.edifactparser.parser import EdifactParser


class TestEdifactParser(unittest.TestCase):
    """Test case for the EdifactParser class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.parser = EdifactParser()
        self.samples_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))) / "samples"

        # APERAK sample files
        self.aperak_sample_file_path_request = self.samples_dir / "aperak-message-example-request.txt"
        self.aperak_sample_file_path_response = self.samples_dir / "aperak-message-example-response.json"
        self.aperak_sample_file_path_request_with_invalid_una = (
                self.samples_dir / "aperak-message-example-with-invalid-una-request.txt"
        )
        self.aperak_sample_file_path_response_with_invalid_una = (
                self.samples_dir / "aperak-message-example-with-invalid-una-response.json"
        )

        # MSCONS sample files
        self.mscons_sample_file_path_request = self.samples_dir / "mscons-message-example-request.txt"
        self.mscons_sample_file_path_response = self.samples_dir / "mscons-message-example-response.json"
        self.mscons_sample_file_path_request_with_una_spec = self.samples_dir / "mscons-message-example-una-spec-requset.txt"
        self.mscons_sample_file_path_response_with_una_spec = self.samples_dir / "mscons-message-example-una-spec-response.json"

    def test_init(self):
        """Test that the parser initializes correctly."""
        self.assertIsNotNone(self.parser._EdifactParser__handler_factory)
        self.assertIsNotNone(self.parser._EdifactParser__resolver_factory)
        # Context is private, so we don't test it directly

    def test_parse_empty_string(self):
        """Test parsing an empty string."""
        # Act & Assert
        with self.assertRaises(EdifactParserException):
            self.parser.parse("")

    def test_parse_aperak_sample_file(self):
        """Test that the parser can parse the APERAK sample file."""
        # Read the sample file
        with open(self.aperak_sample_file_path_request, encoding='utf-8') as f:
            edifact_data = f.read()

        # Parse the data
        parsed_object = self.parser.parse(edifact_data)

        # Verify some basic properties
        self.assertIsNotNone(parsed_object)
        self.assertEqual(parsed_object.unz_nutzdaten_endsegment.datenaustauschzaehler, 1)
        self.assertEqual(len(parsed_object.unh_unt_nachrichten), 1)

    def test_parse_aperak_sample_file_with_invalid_una_segment(self):
        """Test that the parser can parse the APERAK sample file with an invalid UNA segment."""
        # Read the sample file
        with open(self.aperak_sample_file_path_request_with_invalid_una, encoding='utf-8') as f:
            edifact_data = f.read()

        # Parse the data
        parsed_object = self.parser.parse(edifact_data)

        # Verify some basic properties
        self.assertIsNotNone(parsed_object)
        self.assertEqual(parsed_object.unz_nutzdaten_endsegment.datenaustauschzaehler, 1)
        self.assertEqual(len(parsed_object.unh_unt_nachrichten), 1)

    def test_parse_mscons_sample_file(self):
        """Test that the parser can parse the MSCONS sample file."""
        # Read the sample file
        with open(self.mscons_sample_file_path_request, encoding='utf-8') as f:
            edifact_data = f.read()

        # Parse the data
        parsed_object = self.parser.parse(edifact_data)

        # Verify some basic properties
        self.assertIsNotNone(parsed_object)
        self.assertEqual(parsed_object.unz_nutzdaten_endsegment.datenaustauschzaehler, 2)
        self.assertEqual(len(parsed_object.unh_unt_nachrichten), 2)

    def test_parse_mscons_sample_file_with_invalid_una_segment(self):
        """Test that the parser can parse a MSCONS file with an invalid UNA segment (UNA segment with a prefix)."""
        # Read the sample file
        with open(self.mscons_sample_file_path_request_with_una_spec, encoding='utf-8') as f:
            edifact_data = f.read()

        # Add a prefix to the UNA segment to simulate an invalid UNA segment
        modified_edifact_data = edifact_data.replace("UNA:+,? '", "[CUSTOM_PREFIX]:UNA:+,? '")

        # Parse the data
        parsed_object = self.parser.parse(modified_edifact_data)

        # Verify some basic properties
        self.assertIsNotNone(parsed_object)
        self.assertEqual(parsed_object.unz_nutzdaten_endsegment.datenaustauschzaehler, 2)
        self.assertEqual(len(parsed_object.unh_unt_nachrichten), 2)

    def test_parse_aperak_sample_file_full_content(self):
        """Test that the parser can parse the APERAK sample file and match the expected JSON response."""
        # Read the sample file and expected response
        with open(self.aperak_sample_file_path_request, encoding='utf-8') as f:
            edifact_data = f.read()

        with open(self.aperak_sample_file_path_response, encoding='utf-8') as f:
            expected_response = json.load(f)

        # Parse the data
        parsed_object = self.parser.parse(edifact_data)

        # Convert the parsed object to a dictionary for comparison
        parsed_dict = parsed_object.model_dump()

        # Verify the full content matches the expected response
        self.assertEqual(expected_response, parsed_dict)

    def test_parse_mscons_sample_file_full_content(self):
        """Test that the parser can parse the MSCONS sample file and match the expected JSON response."""
        # Read the sample file and expected response
        with open(self.mscons_sample_file_path_request, encoding='utf-8') as f:
            edifact_data = f.read()

        with open(self.mscons_sample_file_path_response, encoding='utf-8') as f:
            expected_response = json.load(f)

        # Parse the data
        parsed_object = self.parser.parse(edifact_data)

        # Convert the parsed object to a dictionary for comparison
        parsed_dict = parsed_object.model_dump()

        # Verify the full content matches the expected response
        self.assertEqual(expected_response, parsed_dict)


    def test_parse_mscons_sample_file_with_una_spec(self):
        """Test that the parser can parse a MSCONS file with a UNA segment specifying custom delimiters."""
        # Read the sample file
        with open(self.mscons_sample_file_path_request_with_una_spec, encoding='utf-8') as f:
            edifact_data = f.read()

        # Parse the data
        parsed_object = self.parser.parse(edifact_data)

        # Verify some basic properties
        self.assertIsNotNone(parsed_object)
        self.assertEqual(parsed_object.unz_nutzdaten_endsegment.datenaustauschzaehler, 2)
        self.assertEqual(len(parsed_object.unh_unt_nachrichten), 2)

        # Verify that the UNA segment was found and initialized correctly
        self.assertIsNotNone(parsed_object.una_service_string_advice)
        self.assertEqual(":", parsed_object.una_service_string_advice.component_separator)
        self.assertEqual("+", parsed_object.una_service_string_advice.element_separator)
        self.assertEqual(",", parsed_object.una_service_string_advice.decimal_mark)
        self.assertEqual("?", parsed_object.una_service_string_advice.release_character)
        self.assertEqual(" ", parsed_object.una_service_string_advice.reserved)
        self.assertEqual("'", parsed_object.una_service_string_advice.segment_terminator)


if __name__ == '__main__':
    unittest.main()
