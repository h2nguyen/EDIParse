# coding: utf-8

"""
Main application module for the EDIFACT parser REST API.

This module serves as the entry point for the EDIFACT parser application,
setting up the FastAPI application with appropriate routes, event handlers,
and logging configuration. It provides a REST API for parsing EDIFACT messages
(e.g., MSCONS, APERAK, ect. format) used in the energy sector (DE/AT/CH).

The API follows the OpenAPI specification.
"""  # noqa: E501
import logging.config

from fastapi.responses import RedirectResponse

from ediparse.adapters.inbound.rest import main
from ediparse.adapters.inbound.rest.impl.health_check_routers import router as HealthChecksApiRouter
from ediparse.adapters.inbound.rest.impl.lifespan_events import startup_lifespan
from ediparse.infrastructure.logging_config import get_logging_config

logging.config.dictConfig(get_logging_config())

app = main.app

# Add event handler during application startup
app.add_event_handler("startup", startup_lifespan)

# Make a redirect to the swagger-ui docs when accessing the base url
@app.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url=str(app.docs_url))

app.include_router(HealthChecksApiRouter)
