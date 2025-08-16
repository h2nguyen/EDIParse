import unittest
from unittest.mock import MagicMock

from ediparse.adapters.inbound.rest.impl.health_check_filters import HealthEndpointsFilter


class TestHealthEndpointsFilter(unittest.TestCase):
    """Test cases for the HealthEndpointsFilter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.filter = HealthEndpointsFilter()

    def test_filter_allows_non_health_messages(self):
        """Test that the filter allows messages not related to health endpoints."""
        record = MagicMock()
        record.getMessage.return_value = "Some regular log message"

        result = self.filter.filter(record)

        self.assertTrue(result, "Filter should allow non-health endpoint messages")

    def test_filter_blocks_health_200_messages(self):
        """Test that the filter blocks 200 status messages from health endpoints."""
        test_cases = [
            "GET /health/readiness HTTP/1.1 200",
            "GET /health/liveness HTTP/1.1 200",
            "GET /metrics HTTP/1.1 200"
        ]

        for message in test_cases:
            record = MagicMock()
            record.getMessage.return_value = message

            result = self.filter.filter(record)

            self.assertFalse(result, f"Filter should block health endpoint 200 message: {message}")

    def test_filter_allows_health_non_200_messages(self):
        """Test that the filter allows non-200 status messages from health endpoints."""
        test_cases = [
            "GET /health/readiness HTTP/1.1 500",
            "GET /health/liveness HTTP/1.1 404",
            "GET /metrics HTTP/1.1 503"
        ]

        for message in test_cases:
            record = MagicMock()
            record.getMessage.return_value = message

            result = self.filter.filter(record)

            self.assertTrue(result, f"Filter should allow health endpoint non-200 message: {message}")

    def test_filter_handles_type_error(self):
        """Test that the filter handles TypeError when getMessage() fails."""
        record = MagicMock()
        record.getMessage.side_effect = TypeError("Test error")
        record.msg = "Some message that doesn't match health endpoints"

        result = self.filter.filter(record)

        self.assertTrue(result, "Filter should handle TypeError and use record.msg instead")


if __name__ == "__main__":
    unittest.main()
