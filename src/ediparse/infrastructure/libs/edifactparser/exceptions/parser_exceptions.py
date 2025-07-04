# coding: utf-8
"""
Exceptions related to EDIFACT message parsing.

This module provides exception classes for handling errors during the parsing
of different types of EDIFACT messages, including MSCONS and APERAK formats,
as well as general EDIFACT parsing errors.
"""


class MSCONSParserException(Exception):
    """
    Exception raised for errors specific to MSCONS message parsing.

    MSCONS (Metering Statistics and Consumption) is an EDIFACT message format
    used for transmitting consumption data. This exception is raised when errors
    occur during the parsing of MSCONS messages.

    Attributes:
        message (str): Explanation of the error
        value (str): Additional information about the error
    """
    def __init__(self, message: str = "Parser error", value: str = None):
        self.message = message
        self.value = value
        super().__init__(f"{message}{': ' + value if value else ''}")


class EdifactParserException(Exception):
    """
    Exception raised for general EDIFACT parsing errors.

    This is a general exception for errors that occur during the parsing of
    any EDIFACT message, regardless of the specific message type.

    Attributes:
        message (str): Explanation of the error
        value (str): Additional information about the error
    """
    def __init__(self, message: str = "Parser error", value: str = None):
        self.message = message
        self.value = value
        super().__init__(f"{message}{': ' + value if value else ''}")


class APERAKParserException(Exception):
    """
    Exception raised for errors specific to APERAK message parsing.

    APERAK (Application Error and Acknowledgment) is an EDIFACT message format
    used for reporting errors and acknowledgments. This exception is raised when
    errors occur during the parsing of APERAK messages.

    Attributes:
        message (str): Explanation of the error
        value (str): Additional information about the error
    """
    def __init__(self, message: str = "Parser error", value: str = None):
        self.message = message
        self.value = value
        super().__init__(f"{message}{': ' + value if value else ''}")
