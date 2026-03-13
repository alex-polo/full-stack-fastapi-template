import logging
import time
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from fastapi import Request, Response

log = logging.getLogger(__name__)


async def request_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Add request ID for tracing."""
    request_id: str = request.headers.get(
        "X-Request-ID", f"req_{uuid.uuid4().hex[:12]}"
    )
    try:
        response: Response = await call_next(request)
    except Exception as e:
        log.error(f"[{request_id}] Request failed")
        raise e
    response.headers["X-Request-ID"] = request_id
    return response


async def timing_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Add process time header."""
    start_time: float = time.time()
    response: Response = await call_next(request)
    process_time: float = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.3f}s"
    return response


async def logging_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Log each request with request ID and timing."""
    start_time: float = time.time()

    try:
        response: Response = await call_next(request)
    except Exception as e:
        request_id: str = getattr(request.state, "request_id", "unknown")
        log.error("[%s] Request failed", request_id)
        raise e

    request_id: str = response.headers.get("X-Request-ID", "unknown")
    process_time: float = time.time() - start_time
    log.info(
        "[%s] %s %s → %s (%.3fs)",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )
    return response
