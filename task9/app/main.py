
from __future__ import annotations

import platform
import subprocess
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, Request, Response, status
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest


PING_ADDRESS = "77.88.8.8"
PING_TIMEOUT_SECONDS = 2

app = FastAPI(title="Task 9 service", version="1.0.0")

HTTP_REQUESTS_TOTAL = Counter(
    "task9_http_requests_total",
    "Total number of HTTP requests handled by the Task 9 application.",
    ["method", "path", "status_code"],
)
PING_HEALTH = Gauge(
    "task9_ping_health",
    "Whether 77.88.8.8 answered the latest ICMP ping (1 for success, 0 for failure).",
)
PING_HEALTH.set(float("nan"))


@app.middleware("http")
async def record_request_metric(request: Request, call_next):
    """Count requests using route templates instead of arbitrary URL paths."""

    response = await call_next(request)
    route = request.scope.get("route")
    path = getattr(route, "path", "unmatched")
    HTTP_REQUESTS_TOTAL.labels(
        method=request.method,
        path=path,
        status_code=str(response.status_code),
    ).inc()
    return response


def build_ping_command() -> list[str]:
    """Build the ping command for Windows or Linux."""

    if platform.system().lower() == "windows":
        return [
            "ping",
            "-n",
            "1",
            "-w",
            str(PING_TIMEOUT_SECONDS * 1000),
            PING_ADDRESS,
        ]

    return [
        "ping",
        "-c",
        "1",
        "-W",
        str(PING_TIMEOUT_SECONDS),
        PING_ADDRESS,
    ]


def ping_target() -> bool:
    """Return True when the configured address answers one ICMP request."""

    try:
        result = subprocess.run(
            build_ping_command(),
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=PING_TIMEOUT_SECONDS + 2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False

    return result.returncode == 0


@app.post("/", response_class=PlainTextResponse)
def hello(test_header: Annotated[str | None, Header(alias="Test")] = None) -> str:
    """Return the greeting only for the required Test header."""

    if test_header != "Hello":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return "Hello, World!"


@app.get("/health", response_class=PlainTextResponse)
def health() -> PlainTextResponse:
    """Report whether 77.88.8.8 is reachable with ICMP ping."""

    if ping_target():
        PING_HEALTH.set(1)
        return PlainTextResponse("OK", status_code=status.HTTP_200_OK)

    PING_HEALTH.set(0)
    return PlainTextResponse(
        "Service Unavailable",
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    """Expose application metrics in the Prometheus text format."""

    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
