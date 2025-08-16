import unittest
from unittest.mock import MagicMock

from ediparse.application.services.parser_service import ParserService
from ediparse.application.usecases.parse_message_usecase import ParseMessageUseCase


class TestParserService(unittest.TestCase):
    """Test cases for the ParserService class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_parse_message_usecase = MagicMock(spec=ParseMessageUseCase)
        self.parser_service = ParserService(parse_message_usecase=self.mock_parse_message_usecase)

    def test_init_with_parse_message_usecase(self):
        """Test that the service can be initialized with a parse message usecase."""
        self.assertEqual(self.parser_service._ParserService__parse_message_usecase, self.mock_parse_message_usecase)

    def test_init_without_parse_message_usecase(self):
        """Test that the service creates a new parse message usecase if none is provided."""
        with unittest.mock.patch(
                'ediparse.application.services.parser_service.ParseMessageUseCase') as mock_parse_message_usecase_class:
            mock_parse_message_usecase_instance = MagicMock(spec=ParseMessageUseCase)
            mock_parse_message_usecase_class.return_value = mock_parse_message_usecase_instance

            parser_service = ParserService()

            self.assertEqual(parser_service._ParserService__parse_message_usecase, mock_parse_message_usecase_instance)
            mock_parse_message_usecase_class.assert_called_once()

    def test_parse_message(self):
        """Test that parse_message calls the parse message usecase's execute method with the correct arguments."""
        # Setup
        message_content = "test_message_content"
        max_lines_to_parse = 10
        expected_result = MagicMock()
        self.mock_parse_message_usecase.execute.return_value = expected_result

        # Execute
        result = self.parser_service.parse_message(message_content=message_content,
                                                   max_lines_to_parse=max_lines_to_parse)

        # Verify
        self.assertEqual(result, expected_result)
        self.mock_parse_message_usecase.execute.assert_called_once_with(
            edifact_specific_message_content=message_content,
            max_lines_to_parse=max_lines_to_parse
        )


if __name__ == "__main__":
    unittest.main()
