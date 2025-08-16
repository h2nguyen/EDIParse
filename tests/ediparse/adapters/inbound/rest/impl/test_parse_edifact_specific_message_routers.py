import unittest
from unittest.mock import patch, MagicMock

import pytest
from fastapi import status
from starlette.responses import JSONResponse

from ediparse.adapters.inbound.rest.impl.parse_edifact_specific_message_routers import ParseEdifactMessageRouter
from ediparse.infrastructure.libs.edifactparser.exceptions import CONTRLException, EdifactParserException


class TestParseEdifactMessageRouter(unittest.TestCase):
    """Test cases for the ParseEdifactMessageRouter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_parser_service = MagicMock()
        self.router = ParseEdifactMessageRouter(parser_service=self.mock_parser_service)

    def test_init_with_parser(self):
        """Test that the router can be initialized with a parser service."""
        self.assertEqual(self.router._ParseEdifactMessageRouter__parser_service, self.mock_parser_service)

    @patch('ediparse.adapters.inbound.rest.impl.parse_edifact_specific_message_routers.ParserService')
    def test_init_without_parser(self, mock_parser_service_class):
        """Test that the router creates a new parser service if none is provided."""
        mock_parser_service_instance = MagicMock()
        mock_parser_service_class.return_value = mock_parser_service_instance

        router = ParseEdifactMessageRouter()

        self.assertEqual(router._ParseEdifactMessageRouter__parser_service, mock_parser_service_instance)
        mock_parser_service_class.assert_called_once()

    @pytest.mark.asyncio
    @patch('time.perf_counter')
    async def test_parse_string_input_success(self, mock_perf_counter):
        """Test that parse_string_input returns parsed data on success."""
        # Setup
        mock_perf_counter.side_effect = [1.0, 2.0]  # t1=1.0, t2=2.0
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        edifact_input = "test_edifact_data"
        limit_mode = False

        # Execute
        response = await self.router.parse_string_input(limit_mode, edifact_input)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content=edifact_input,
                                                                       max_lines_to_parse=-1)
        mock_parsed_obj.model_dump.assert_called_once()

    @pytest.mark.asyncio
    @patch('time.perf_counter')
    @patch('ediparse.adapters.inbound.rest.impl.parse_edifact_specific_message_routers.logger')
    async def test_parse_string_input_logs_performance(self, mock_logger, mock_perf_counter):
        """Test that parse_string_input logs performance metrics."""
        # Setup
        mock_perf_counter.side_effect = [1.0, 3.5]  # t1=1.0, t2=3.5 (2.5s difference)
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        limit_mode = False

        # Execute
        await self.router.parse_string_input(limit_mode, "test_data")

        # Verify
        mock_logger.info.assert_called_once_with("SPEED-TEST: Parsing took 2.50s")

    @pytest.mark.asyncio
    async def test_parse_string_input_contrl_exception(self):
        """Test that parse_string_input handles CONTRLException correctly."""
        # Setup
        error_message = "CONTRL error message"
        self.mock_parser_service.parse_message.side_effect = CONTRLException(error_message)
        limit_mode = False

        # Execute
        response = await self.router.parse_string_input(limit_mode, "invalid_data")

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_parse_string_input_edifact_parser_exception(self):
        """Test that parse_string_input handles EdifactParserException correctly."""
        # Setup
        error_message = "EDIFACT parser error message"
        self.mock_parser_service.parse_message.side_effect = EdifactParserException(error_message)
        limit_mode = False

        # Execute
        response = await self.router.parse_string_input(limit_mode, "invalid_data")

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    @patch('time.perf_counter')
    async def test_parse_file_success(self, mock_perf_counter):
        """Test that parse_file returns parsed data on success."""
        # Setup
        mock_perf_counter.side_effect = [1.0, 2.0]  # t1=1.0, t2=2.0
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        edifact_file = "test_edifact_data"
        limit_mode = False

        # Execute
        response = await self.router.parse_file(limit_mode, edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content=edifact_file,
                                                                       max_lines_to_parse=-1)
        mock_parsed_obj.model_dump.assert_called_once()

    @pytest.mark.asyncio
    async def test_parse_file_no_file(self):
        """Test that parse_file handles no file provided correctly."""
        # Setup
        edifact_file = None
        limit_mode = False

        # Execute
        response = await self.router.parse_file(limit_mode, edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), '{"error_message":"No file provided"}')

    @pytest.mark.asyncio
    async def test_parse_file_contrl_exception(self):
        """Test that parse_file handles CONTRLException correctly."""
        # Setup
        error_message = "CONTRL error message"
        self.mock_parser_service.parse_message.side_effect = CONTRLException(error_message)
        edifact_file = "invalid_data"
        limit_mode = False

        # Execute
        response = await self.router.parse_file(limit_mode, edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_parse_file_edifact_parser_exception(self):
        """Test that parse_file handles EdifactParserException correctly."""
        # Setup
        error_message = "EDIFACT parser error message"
        self.mock_parser_service.parse_message.side_effect = EdifactParserException(error_message)
        edifact_file = "invalid_data"
        limit_mode = False

        # Execute
        response = await self.router.parse_file(limit_mode, edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_parse_file_bytes(self):
        """Test that parse_file handles bytes content correctly."""
        # Setup
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        edifact_file = b"test_edifact_data"
        limit_mode = False

        # Execute
        response = await self.router.parse_file(limit_mode, edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content="test_edifact_data",
                                                                       max_lines_to_parse=-1)

    @pytest.mark.asyncio
    async def test_parse_file_tuple(self):
        """Test that parse_file handles tuple content correctly."""
        # Setup
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        edifact_file = ("filename.txt", b"test_edifact_data")
        limit_mode = False

        # Execute
        response = await self.router.parse_file(limit_mode, edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content="test_edifact_data",
                                                                       max_lines_to_parse=-1)

    @pytest.mark.asyncio
    @patch('time.strftime')
    @patch('time.perf_counter')
    async def test_download_parsed_string_input_success(self, mock_perf_counter, mock_strftime):
        """Test that download_parsed_string_input returns downloadable JSON on success."""
        # Setup
        mock_perf_counter.side_effect = [1.0, 2.0]  # t1=1.0, t2=2.0
        mock_strftime.return_value = "20230101_120000"
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        edifact_input = "test_edifact_data"

        # Execute
        response = await self.router.download_parsed_string_input(edifact_input)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.assertEqual(response.headers["Content-Disposition"],
                         "attachment; filename=edifact_message_parsed_20230101_120000.json")
        self.mock_parser_service.parse_message.assert_called_once_with(message_content=edifact_input,
                                                                       max_lines_to_parse=-1)
        mock_parsed_obj.model_dump.assert_called_once()

    @pytest.mark.asyncio
    async def test_download_parsed_string_input_contrl_exception(self):
        """Test that download_parsed_string_input handles CONTRLException correctly."""
        # Setup
        error_message = "CONTRL error message"
        self.mock_parser_service.parse_message.side_effect = CONTRLException(error_message)

        # Execute
        response = await self.router.download_parsed_string_input("invalid_data")

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_download_parsed_string_input_edifact_parser_exception(self):
        """Test that download_parsed_string_input handles EdifactParserException correctly."""
        # Setup
        error_message = "EDIFACT parser error message"
        self.mock_parser_service.parse_message.side_effect = EdifactParserException(error_message)

        # Execute
        response = await self.router.download_parsed_string_input("invalid_data")

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    @patch('time.strftime')
    @patch('time.perf_counter')
    async def test_download_parsed_file_success(self, mock_perf_counter, mock_strftime):
        """Test that download_parsed_file returns downloadable JSON on success."""
        # Setup
        mock_perf_counter.side_effect = [1.0, 2.0]  # t1=1.0, t2=2.0
        mock_strftime.return_value = "20230101_120000"
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        edifact_file = "test_edifact_data"

        # Execute
        response = await self.router.download_parsed_file(edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.assertEqual(response.headers["Content-Disposition"],
                         "attachment; filename=edifact_message_parsed_20230101_120000.json")
        self.mock_parser_service.parse_message.assert_called_once_with(message_content=edifact_file,
                                                                       max_lines_to_parse=-1)
        mock_parsed_obj.model_dump.assert_called_once()

    @pytest.mark.asyncio
    async def test_download_parsed_file_no_file(self):
        """Test that download_parsed_file handles no file provided correctly."""
        # Setup
        edifact_file = None

        # Execute
        response = await self.router.download_parsed_file(edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), '{"error_message":"No file provided"}')

    @pytest.mark.asyncio
    async def test_download_parsed_file_contrl_exception(self):
        """Test that download_parsed_file handles CONTRLException correctly."""
        # Setup
        error_message = "CONTRL error message"
        self.mock_parser_service.parse_message.side_effect = CONTRLException(error_message)
        edifact_file = "invalid_data"

        # Execute
        response = await self.router.download_parsed_file(edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_download_parsed_file_edifact_parser_exception(self):
        """Test that download_parsed_file handles EdifactParserException correctly."""
        # Setup
        error_message = "EDIFACT parser error message"
        self.mock_parser_service.parse_message.side_effect = EdifactParserException(error_message)
        edifact_file = "invalid_data"

        # Execute
        response = await self.router.download_parsed_file(edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_download_parsed_file_bytes(self):
        """Test that download_parsed_file handles bytes content correctly."""
        # Setup
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        edifact_file = b"test_edifact_data"

        # Execute
        response = await self.router.download_parsed_file(edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content="test_edifact_data",
                                                                       max_lines_to_parse=-1)

    @pytest.mark.asyncio
    async def test_download_parsed_file_tuple(self):
        """Test that download_parsed_file handles tuple content correctly."""
        # Setup
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        edifact_file = ("filename.txt", b"test_edifact_data")

        # Execute
        response = await self.router.download_parsed_file(edifact_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content="test_edifact_data",
                                                                       max_lines_to_parse=-1)


if __name__ == "__main__":
    unittest.main()
