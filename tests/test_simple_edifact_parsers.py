import os
import unittest
from pathlib import Path

from ediparse.libs.edifactparser.parser import EdifactParser


class TestSimpleEdifactParsers(unittest.TestCase):
    """A simple test case to demonstrate testing in this project."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.parser = EdifactParser()
        self.samples_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "tests" / "samples"
        self.aperak_sample_file_path_request = self.samples_dir / "aperak-message-example-request.txt"
        self.mscons_sample_file_path_request = self.samples_dir / "mscons-message-example-request.txt"

    def test_parse_aperak_sample_file(self):
        """Test that the parser can parse the sample file."""
        # Read the sample file
        file_path = self.aperak_sample_file_path_request

        with open(file_path, encoding='utf-8') as f:
            edifact_data = f.read()

        # Parse the data
        parsed_object = self.parser.parse(edifact_data)

        # Verify some basic properties
        self.assertIsNotNone(parsed_object)
        self.assertEqual(parsed_object.unz_nutzdaten_endsegment.datenaustauschzaehler, 1)
        self.assertEqual(len(parsed_object.unh_unt_nachrichten), 1)

    def test_parse_mscons_sample_file(self):
        """Test that the parser can parse the sample file."""
        # Read the sample file
        file_path = self.mscons_sample_file_path_request

        with open(file_path, encoding='utf-8') as f:
            edifact_data = f.read()

        # Parse the data
        parsed_object = self.parser.parse(edifact_data)

        # Verify some basic properties
        self.assertIsNotNone(parsed_object)
        self.assertEqual(parsed_object.unz_nutzdaten_endsegment.datenaustauschzaehler, 2)
        self.assertEqual(len(parsed_object.unh_unt_nachrichten), 2)


if __name__ == '__main__':
    unittest.main()
