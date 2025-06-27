# coding: utf-8
"""
Package for inbound ports.

This package contains interfaces (ports) that allow external systems to
interact with the application. Inbound ports define the operations that
the application exposes to the outside world, following the Ports and
Adapters (Hexagonal) architecture pattern.

The package includes:
- MessageParserPort: Interface for parsing EDIFACT messages
"""

from ediparse.domain.ports.inbound.message_parser_port import MessageParserPort

__all__ = ["MessageParserPort"]
