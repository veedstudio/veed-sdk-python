# Code generated from the VEED OpenAPI spec. DO NOT EDIT.

from __future__ import annotations

from typing import Any, List, Optional

# The server chooses Retry-After and no timeout covers a sleep, so an unclamped
# header is a remote hang.
MAX_RETRY_AFTER = 60.0


class VeedError(Exception):
    pass


class APIConnectionError(VeedError):
    pass


class APIError(VeedError):
    """HTTP-layer error: the request itself was rejected. For submits this
    means no job was created (per the API contract)."""

    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        request_id: str,
        details: Optional[List[Any]] = None,
        retry_after: float = 0.0,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.request_id = request_id
        self.details = details or []
        self.retry_after = retry_after
        super().__init__(f"veed: {status_code} {code}: {message} (request_id: {request_id})")


class InvalidRequestError(APIError):
    pass


class AuthenticationError(APIError):
    pass


class PermissionDeniedError(APIError):
    pass


class NotFoundError(APIError):
    pass


class RateLimitError(APIError):
    pass


class InternalServerError(APIError):
    pass


_STATUS_MAP = {
    400: InvalidRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    422: InvalidRequestError,
    429: RateLimitError,
}


def error_from_response(resp: Any) -> APIError:
    status = resp.status_code
    cls = _STATUS_MAP.get(status)
    if cls is None:
        cls = InternalServerError if status >= 500 else APIError
    code = ""
    message = ""
    details = None
    request_id = resp.headers.get("X-Request-ID", "")
    try:
        body = resp.json().get("error") or {}
        code = body.get("code", "")
        message = body.get("message", "")
        details = body.get("details")
        request_id = body.get("request_id") or request_id
    except Exception:
        message = resp.text[:200]
    retry_after = 0.0
    ra = resp.headers.get("Retry-After")
    if ra and ra.isdigit():
        retry_after = min(float(ra), MAX_RETRY_AFTER)
    return cls(
        status_code=status,
        code=code,
        message=message,
        request_id=request_id,
        details=details,
        retry_after=retry_after,
    )


class JobFailedError(VeedError):
    """Job-layer failure: the job was accepted, but rendering failed. Raised
    by wait/generate, not as an HTTP error. `code` holds the model-specific
    failure code and `job` the final job object."""

    def __init__(self, *, job_id: str, code: str, message: str, details: Any = None, job: Any = None) -> None:
        self.job_id = job_id
        self.code = code
        self.message = message
        self.details = details or []
        self.job = job
        super().__init__(f"veed: job {job_id} failed ({code}): {message}")


class JobCancelledError(VeedError):
    def __init__(self, *, job_id: str, job: Any = None) -> None:
        self.job_id = job_id
        self.job = job
        super().__init__(f"veed: job {job_id} was cancelled")


class WaitTimeoutError(VeedError):
    """wait/generate gave up before the job reached a terminal state. The job
    may still finish server-side; resume with wait(job_id)."""

    def __init__(self, *, job_id: str, timeout: float, job: Any = None) -> None:
        self.job_id = job_id
        self.timeout = timeout
        self.job = job
        super().__init__(
            f"veed: timed out after {timeout}s waiting for job {job_id} (the job may still finish; resume with wait)"
        )
