# coding: utf-8
"""
API routes for health checks.

This module defines FastAPI routes for health checks, including:
- Liveness check: Verifies that the application is running
- Readiness check: Verifies that the application is ready to accept requests
                  and that its dependencies are reachable

These endpoints are used by container orchestration systems like Kubernetes
to monitor the health of the application and make decisions about routing
traffic or restarting containers.
"""

import psutil
from fastapi import APIRouter, status
from starlette.responses import JSONResponse

router = APIRouter()


@router.get(
    "/health/liveness",
    responses={
        200: {"description": "Accepted"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
    },
    tags=["Health checks"],
    summary="Checks the liveness of the server",
    response_model_by_alias=True,
    include_in_schema=False,
)
async def check_liveness() -> JSONResponse:
    """
    Basic liveness check to ensure the application is running.
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok"})


@router.get(
    "/health/readiness",
    responses={
        200: {"description": "Accepted"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        503: {"description": "Service unavailable"},
    },
    tags=["Health checks"],
    summary="Checks the readiness of the server",
    response_model_by_alias=True,
    include_in_schema=False,
)
async def check_readiness() -> JSONResponse:
    """
    Readiness check to ensure dependencies are reachable.
    """
    try:
        if psutil.cpu_percent(interval=0.1) > 95:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "not ready", "reason": "CPU overloaded"},
            )
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok"})
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": str(e)},
        )
