import unittest
from unittest.mock import MagicMock

import pytest
from fastapi import status
from starlette.responses import JSONResponse

from ediparse.adapters.inbound.rest.impl.parse_edifact_specific_message_routers import ParseEdifactMessageRouter


class TestEdifactMessageFileEncoding(unittest.TestCase):
    """Test cases for handling different file encodings in ParseEdifactMessageRouter."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_parser_service = MagicMock()
        self.router = ParseEdifactMessageRouter(parser_service=self.mock_parser_service)

    @pytest.mark.asyncio
    async def test_parse_file_with_non_utf8_encoding(self):
        """Test that parse_file can handle files with non-UTF-8 encoding."""
        # Setup
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj

        # Create a bytes object that will fail UTF-8 decoding but succeed with ISO-8859-1
        # The byte 0xe4 is valid in ISO-8859-1 (ä) but invalid in UTF-8 as a standalone byte
        non_utf8_content = b"UNA:+.? 'UNB+UNOC:3+9904935000\xe4"
        limit_mode = False

        # Execute
        response = await self.router.parse_file(limit_mode, non_utf8_content)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"key":"value"}')

        # Verify that the content was decoded with ISO-8859-1 after UTF-8 failed
        # The expected string should contain the ISO-8859-1 character ä (0xe4)
        expected_decoded = "UNA:+.? 'UNB+UNOC:3+9904935000ä"
        self.mock_parser_service.parse_message.assert_called_once_with(
            message_content=expected_decoded,
            max_lines_to_parse=-1
        )

    @pytest.mark.asyncio
    async def test_download_parsed_file_with_non_utf8_encoding(self):
        """Test that download_parsed_file can handle files with non-UTF-8 encoding."""
        # Setup
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj

        # Create a bytes object that will fail UTF-8 decoding but succeed with ISO-8859-1
        non_utf8_content = b"UNA:+.? 'UNB+UNOC:3+9904935000\xe4"

        # Execute
        response = await self.router.download_parsed_file(non_utf8_content)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.assertIn("Content-Disposition", response.headers)
        self.assertIn("attachment; filename=edifact_message_parsed_", response.headers["Content-Disposition"])

        # Verify that the content was decoded with ISO-8859-1 after UTF-8 failed
        expected_decoded = "UNA:+.? 'UNB+UNOC:3+9904935000ä"
        self.mock_parser_service.parse_message.assert_called_once_with(
            message_content=expected_decoded,
            max_lines_to_parse=-1
        )


if __name__ == "__main__":
    unittest.main()
