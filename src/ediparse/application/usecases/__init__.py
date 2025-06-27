# coding: utf-8
"""
Package for application use cases.

This package contains use case classes that implement the application's business logic.
Use cases represent the specific actions or operations that the application can perform,
and they orchestrate the flow of data between the domain entities and the external world.

The package includes:
- ParseMessageUseCase: Use case for parsing EDIFACT messages using the EDIFACT parser
"""

from ediparse.application.usecases.parse_message_usecase import ParseMessageUseCase

__all__ = ["ParseMessageUseCase"]
