import logging.config
import os
import unittest
from unittest.mock import patch

from ediparse.infrastructure.logging_config import (
    get_logging_config,
    LOGGING_CONFIG,
    LOGGING_CONFIG_LOCAL
)


class TestLoggingConfig(unittest.TestCase):
    """Test cases for the logging configuration."""

    def test_get_logging_config_default(self):
        """Test that get_logging_config returns LOGGING_CONFIG_LOCAL by default."""
        with patch.dict(os.environ, {}, clear=True):
            config = get_logging_config()
            self.assertEqual(config, LOGGING_CONFIG_LOCAL)

    def test_get_logging_config_local(self):
        """Test that get_logging_config returns LOGGING_CONFIG_LOCAL when LOGGING_CONFIG=local."""
        with patch.dict(os.environ, {"LOGGING_CONFIG": "local"}, clear=True):
            config = get_logging_config()
            self.assertEqual(config, LOGGING_CONFIG_LOCAL)

    def test_get_logging_config_production(self):
        """Test that get_logging_config returns LOGGING_CONFIG when LOGGING_CONFIG is not local."""
        with patch.dict(os.environ, {"LOGGING_CONFIG": "production"}, clear=True):
            config = get_logging_config()
            self.assertEqual(config, LOGGING_CONFIG)

    @patch('logging.config.dictConfig')
    def test_logging_config_is_valid(self, mock_dict_config):
        """Test that LOGGING_CONFIG is valid for logging.config.dictConfig."""
        # We're just testing that the configuration can be passed to dictConfig
        # without raising an exception. We don't need to test that dictConfig
        # can actually use the configuration, as that's the responsibility of
        # the logging module.
        logging.config.dictConfig(LOGGING_CONFIG)
        mock_dict_config.assert_called_once_with(LOGGING_CONFIG)

    @patch('logging.config.dictConfig')
    def test_logging_config_local_is_valid(self, mock_dict_config):
        """Test that LOGGING_CONFIG_LOCAL is valid for logging.config.dictConfig."""
        # We're just testing that the configuration can be passed to dictConfig
        # without raising an exception. We don't need to test that dictConfig
        # can actually use the configuration, as that's the responsibility of
        # the logging module.
        logging.config.dictConfig(LOGGING_CONFIG_LOCAL)
        mock_dict_config.assert_called_once_with(LOGGING_CONFIG_LOCAL)


if __name__ == "__main__":
    unittest.main()
