# coding: utf-8

import logging
import re


class HealthEndpointsFilter(logging.Filter):
    """
    A logging filter that suppresses log messages for successful health endpoint calls.

    This filter prevents logging of 200 status responses from readiness, liveness, 
    and metrics endpoints to reduce noise in the logs.
    """

    def filter(self, record: logging.LogRecord):
        """
        Filter log records based on their content.

        Args:
            record (logging.LogRecord): The log record to be filtered

        Returns:
            bool: False if the log should be filtered out (suppressed), True otherwise
        """
        try:
            message = record.getMessage()
        except TypeError:
            message = record.msg
        return not re.match(r".*readiness.*200|.*liveness.*200|.*metrics.*200", message)
