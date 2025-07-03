# coding: utf-8
"""
Exceptions related to CONTRL message processing.

CONTRL messages are used in EDIFACT for syntax checking and acknowledgment.
This module provides exception classes for handling errors during CONTRL message processing.
"""


class CONTRLException(Exception):
    """
    Exception raised for errors during CONTRL message processing.

    CONTRL messages are used for syntax checking of EDIFACT messages.
    This exception is raised when syntax errors are detected during
    the processing of CONTRL messages.

    Attributes:
        message (str): Explanation of the error
        value (str): Additional information about the error
    """
    def __init__(self, message: str = "CONTRL – Syntax-Check - Message contains syntax error", value: str = None):
        self.message = message
        self.value = value
        super().__init__(f"{message}{': ' + value if value else ''}")
