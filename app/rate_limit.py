import time
from collections import defaultdict

from fastapi import HTTPException, Request, status

WINDOW_SECONDS = 60
MAX_REQUESTS_PER_WINDOW = 20

_requests: dict[str, list[float]] = defaultdict(list)


def rate_limit(request: Request) -> None:
    client_ip = request.client.host if request.client else "unknown"
    now = time.monotonic()
    window_start = now - WINDOW_SECONDS

    timestamps = _requests[client_ip]
    while timestamps and timestamps[0] < window_start:
        timestamps.pop(0)

    if len(timestamps) >= MAX_REQUESTS_PER_WINDOW:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests, please slow down",
        )

    timestamps.append(now)
