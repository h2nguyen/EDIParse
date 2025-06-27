# coding: utf-8
"""
Package for application services.

This package contains service classes that implement the business logic of the
application. Services coordinate the flow of data between the domain layer and
the adapters, and orchestrate domain objects to perform specific tasks.

The package includes:
- ParserService: Service for parsing EDIFACT messages using the EDIFACT parser
"""

from ediparse.application.services.parser_service import ParserService

__all__ = ["ParserService"]
