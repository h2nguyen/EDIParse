import unittest
from unittest.mock import patch

from fastapi import status
from starlette.responses import JSONResponse

from ediparse.adapters.inbound.rest.impl.health_check_routers import check_liveness, check_readiness


class TestHealthCheckRouters(unittest.TestCase):
    """Test cases for the health check router functions."""

    async def test_check_liveness(self):
        """Test that check_liveness returns a 200 OK response with status 'ok'."""
        response = await check_liveness()

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"status":"ok"}')

    @patch('psutil.cpu_percent')
    async def test_check_readiness_ok(self, mock_cpu_percent):
        """Test that check_readiness returns a 200 OK response when CPU is not overloaded."""
        mock_cpu_percent.return_value = 50.0  # CPU at 50%

        response = await check_readiness()

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"status":"ok"}')
        mock_cpu_percent.assert_called_once_with(interval=0.1)

    @patch('psutil.cpu_percent')
    async def test_check_readiness_cpu_overload(self, mock_cpu_percent):
        """Test that check_readiness returns a 503 Service Unavailable response when CPU is overloaded."""
        mock_cpu_percent.return_value = 96.0  # CPU at 96%, over the 95% threshold

        response = await check_readiness()

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.body.decode(), '{"status":"not ready","reason":"CPU overloaded"}')
        mock_cpu_percent.assert_called_once_with(interval=0.1)

    @patch('psutil.cpu_percent')
    async def test_check_readiness_exception(self, mock_cpu_percent):
        """Test that check_readiness handles exceptions and returns a 503 Service Unavailable response."""
        mock_cpu_percent.side_effect = Exception("Test exception")

        response = await check_readiness()

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.body.decode(), '{"status":"not ready","reason":"Test exception"}')
        mock_cpu_percent.assert_called_once_with(interval=0.1)


if __name__ == "__main__":
    unittest.main()
