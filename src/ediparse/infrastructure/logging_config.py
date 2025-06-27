# coding: utf-8
"""
Logging configuration for the EDIFACT parser.

This module provides logging configuration for the application, with different
settings for production and local development environments. It defines:

- LOGGING_CONFIG: Configuration for production environments with JSON formatting
- LOGGING_CONFIG_LOCAL: Configuration for local development with plain text formatting
- get_logging_config(): Function to select the appropriate configuration based on environment

The logging configuration includes filters to suppress log messages from health
check endpoints to reduce noise in the logs.
"""

import os

from ediparse.adapters.inbound.rest.impl.health_check_filters import HealthEndpointsFilter

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(lineno)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S%z",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "filters": {"health_endpoints_filter": {"()": HealthEndpointsFilter}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": "DEBUG",
            "filters": ["health_endpoints_filter"],
        }
    },
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["console"]},
        "numba": {"level": "INFO", "handlers": ["console"]},
        "httpcore.http11": {"level": "INFO", "handlers": ["console"]},
    },
}

LOGGING_CONFIG_LOCAL = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {
            "format": ("%(levelname)s:%(name)s:%(message)s"),
        }
    },
    "filters": {"health_endpoints_filter": {"()": HealthEndpointsFilter}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain",
            "level": "DEBUG",
            "filters": ["health_endpoints_filter"],
        }
    },
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["console"]},
        "numba": {"level": "INFO", "handlers": ["console"]},
        "httpcore.http11": {"level": "INFO", "handlers": ["console"]},
    },
}


def get_logging_config() -> dict:
    log_env = os.getenv("LOGGING_CONFIG")
    if log_env is not None and log_env != "local":
        return LOGGING_CONFIG
    else:
        return LOGGING_CONFIG_LOCAL
