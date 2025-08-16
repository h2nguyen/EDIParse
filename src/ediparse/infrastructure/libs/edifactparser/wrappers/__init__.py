# coding: utf-8
"""
Package for EDIFACT data structure wrappers.

This package contains classes that wrap the parsed EDIFACT data into structured
object models, making it easier to work with the parsed data. It includes:

- Context classes for maintaining state during parsing
- Constants used throughout the parsing process
- Segment wrappers for different types of EDIFACT segments
- Factory classes for creating context objects
"""
from .context_factory import ParsingContextFactory
