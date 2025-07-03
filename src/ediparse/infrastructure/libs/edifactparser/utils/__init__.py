# coding: utf-8
"""
Package for EDIFACT parsing utility classes.

This package contains utility classes that support the EDIFACT parsing process:

- EdifactSyntaxHelper: Provides methods for parsing and manipulating EDIFACT syntax,
  including splitting segments, elements, and components according to the EDIFACT
  standard's delimiter rules.

- ParsingContextFactory: Creates and manages parsing context objects based on the
  message type being processed, allowing the parser to maintain appropriate state
  during the parsing process.
"""
from .edifact_syntax_helper import EdifactSyntaxHelper
from .context_factory import ParsingContextFactory
