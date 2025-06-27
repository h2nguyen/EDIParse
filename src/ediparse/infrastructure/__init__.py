# coding: utf-8
"""
Infrastructure package for the EDIFACT parser.

This package contains infrastructure components that support the application
but are not part of the core domain logic. It includes cross-cutting concerns
such as logging, configuration, and other technical services.

The package follows the Clean Architecture pattern, where infrastructure
components are in the outermost layer and depend on the inner layers
(domain and application) rather than the other way around.

The package includes:
- logging_config: Configuration for application logging
"""
