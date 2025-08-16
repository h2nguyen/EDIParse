# coding: utf-8
"""
Package for EDIFACT message type-specific modules.

This package contains specialized modules for different EDIFACT message types:
- aperak: Modules for parsing APERAK (Application Error and Acknowledgment) messages
- mscons: Modules for parsing MSCONS (Metering Statistics and Consumption) messages

Each message type has its own context, group state resolver, and segment definitions
tailored to the specific requirements of that message format.
"""

from .module_constants import EdifactMessageType
