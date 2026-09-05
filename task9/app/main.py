
from __future__ import annotations

import platform
import subprocess
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import PlainTextResponse


PING_ADDRESS = "77.88.8.8"
PING_TIMEOUT_SECONDS = 2

app = FastAPI(title="Task 9 service", version="1.0.0")


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
        return PlainTextResponse("OK", status_code=status.HTTP_200_OK)

    return PlainTextResponse(
        "Service Unavailable",
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )
