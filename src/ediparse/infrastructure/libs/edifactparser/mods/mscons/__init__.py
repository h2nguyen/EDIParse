# coding: utf-8
"""
Package for MSCONS (Metering Statistics and Consumption) message parsing.

This package contains specialized modules for parsing MSCONS messages according to
the MSCONS D.04B 2.4c standard. It includes:

- Context classes for maintaining state during MSCONS message parsing
- Group state resolver for determining segment groups in MSCONS messages
- Segment definitions specific to the MSCONS message format

MSCONS messages are used for transmitting consumption data, such as meter readings
and load profiles, between market participants in the energy sector.
"""
