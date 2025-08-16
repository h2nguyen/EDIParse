import unittest
from unittest.mock import patch

from ediparse.adapters.inbound.rest.impl.lifespan_events import startup_lifespan


class TestLifespanEvents(unittest.TestCase):
    """Test cases for the lifespan event functions."""

    @patch('ediparse.adapters.inbound.rest.impl.lifespan_events.logger')
    async def test_startup_lifespan(self, mock_logger):
        """Test that startup_lifespan logs startup message and yields control."""
        # Create an async context manager and use it
        async with startup_lifespan():
            # Check that the logger was called with the expected message
            mock_logger.info.assert_called_once_with("App startup")

            # This code runs inside the context manager, after yield
            pass

        # No additional assertions needed after the context manager exits
        # The test passes if no exceptions are raised


if __name__ == "__main__":
    unittest.main()
