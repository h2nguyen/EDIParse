# coding: utf-8
"""
Package for domain ports.

This package contains interfaces (ports) that define how the application
interacts with external systems. Following the Ports and Adapters (Hexagonal)
architecture pattern, these ports establish clear boundaries between the
domain core and external components.

The package includes:
- inbound: Ports that allow external systems to interact with the application
"""

from ediparse.domain.ports.inbound import MessageParserPort

__all__ = ["MessageParserPort"]
