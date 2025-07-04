import unittest
from unittest.mock import MagicMock

from ediparse.application.usecases.parse_message_usecase import ParseMessageUseCase
from ediparse.domain.ports.inbound import MessageParserPort
from ediparse.infrastructure.libs.edifactparser.parser import EdifactParser


class TestParseMessageUseCase(unittest.TestCase):
    """Test cases for the ParseMessageUseCase class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_parser = MagicMock(spec=EdifactParser)
        self.parse_message_usecase = ParseMessageUseCase(parser=self.mock_parser)

    def test_init_with_parser(self):
        """Test that the use case can be initialized with a parser."""
        self.assertEqual(self.parse_message_usecase._ParseMessageUseCase__parser, self.mock_parser)

    def test_init_without_parser(self):
        """Test that the use case creates a new parser if none is provided."""
        with unittest.mock.patch(
                'ediparse.application.usecases.parse_message_usecase.EdifactParser') as mock_parser_class:
            mock_parser_instance = MagicMock(spec=EdifactParser)
            mock_parser_class.return_value = mock_parser_instance

            parse_message_usecase = ParseMessageUseCase()

            self.assertEqual(parse_message_usecase._ParseMessageUseCase__parser, mock_parser_instance)
            mock_parser_class.assert_called_once()

    def test_execute(self):
        """Test that execute calls the parser's parse method with the correct arguments."""
        # Setup
        message_content = "test_message_content"
        max_lines_to_parse = 10
        expected_result = MagicMock()
        self.mock_parser.parse.return_value = expected_result

        # Execute
        result = self.parse_message_usecase.execute(
            edifact_specific_message_content=message_content,
            max_lines_to_parse=max_lines_to_parse
        )

        # Verify
        self.assertEqual(result, expected_result)
        self.mock_parser.parse.assert_called_once_with(
            edifact_text=message_content,
            max_lines_to_parse=max_lines_to_parse
        )

    def test_implements_message_parser_port(self):
        """Test that ParseMessageUseCase implements the MessageParserPort interface."""
        self.assertIsInstance(self.parse_message_usecase, MessageParserPort)


if __name__ == "__main__":
    unittest.main()
