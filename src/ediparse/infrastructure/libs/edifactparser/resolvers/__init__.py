# coding: utf-8
"""
Package for EDIFACT segment group resolvers.

This package contains classes that determine the segment group context during
EDIFACT message parsing. The resolvers analyze the current segment type and
parsing context to determine which segment group a segment belongs to, ensuring
that segments are properly organized according to the message structure.

The package includes:
- GroupStateResolver: Abstract base class defining the interface for segment group resolvers
- GroupStateResolverFactory: Factory for creating message type-specific resolvers
"""

from .group_state_resolver import GroupStateResolver
from .group_state_resolver_factory import GroupStateResolverFactory
