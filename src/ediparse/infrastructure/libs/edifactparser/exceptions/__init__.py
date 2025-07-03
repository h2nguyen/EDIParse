# coding: utf-8
"""
Package for EDIFACT parser exception classes.

This package contains custom exception classes used throughout the EDIFACT parser:

- CONTRLException: For errors related to CONTRL message syntax checking
- MSCONSParserException: For errors specific to MSCONS message parsing
- EdifactParserException: For general EDIFACT parsing errors
- APERAKParserException: For errors specific to APERAK message parsing
"""
from .contrl_exceptions import CONTRLException
from .parser_exceptions import MSCONSParserException
from .parser_exceptions import EdifactParserException
from .parser_exceptions import APERAKParserException
