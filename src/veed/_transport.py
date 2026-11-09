# Code generated from the VEED OpenAPI spec. DO NOT EDIT.

from __future__ import annotations

import asyncio
import os
import random
import time
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Optional, TypeVar

import httpx

from ._errors import (
    APIConnectionError,
    APIError,
    JobCancelledError,
    JobFailedError,
    RateLimitError,
    VeedError,
    WaitTimeoutError,
    error_from_response,
)
from ._version import VERSION

DEFAULT_BASE_URL = "https://api.veed.io"
DEFAULT_WAIT_TIMEOUT = 900.0

T = TypeVar("T")


@dataclass
class RequestOptions:
    store_io: Optional[bool] = None
    media_expiration_seconds: Optional[int] = None


def _backoff(attempt: int) -> float:
    return random.random() * min(0.5 * (2**attempt), 8.0)


def _retryable(status: int) -> bool:
    # POST retries are safe too: a rejected submit never creates a job.
    return status in (408, 429) or status >= 500


class BaseTransport:
    def __init__(
        self,
        *,
        api_key: Optional[str],
        base_url: Optional[str],
        timeout: float,
        max_retries: int,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("VEED_API_KEY") or ""
        if not self.api_key:
            raise VeedError(
                "veed: missing API key: pass api_key=... or set VEED_API_KEY (create keys in your VEED workspace)"
            )
        self.base_url = (base_url or os.environ.get("VEED_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.store_io = store_io
        self.media_expiration_seconds = media_expiration_seconds

    def _headers(self, options: Optional[RequestOptions]) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "User-Agent": f"veed-sdk-python/{VERSION}",
        }
        store_io = self.store_io
        media_expiration = self.media_expiration_seconds
        if options is not None:
            if options.store_io is not None:
                store_io = options.store_io
            if options.media_expiration_seconds is not None:
                media_expiration = options.media_expiration_seconds
        if store_io is not None:
            headers["X-Veed-Store-IO"] = "1" if store_io else "0"
        if media_expiration is not None:
            headers["X-Veed-Media-Expiration-Seconds"] = str(media_expiration)
        return headers

    @staticmethod
    def _unwrap(resp: httpx.Response) -> Any:
        payload = resp.json()
        if not isinstance(payload, dict) or "data" not in payload:
            raise APIError(
                status_code=resp.status_code,
                code="",
                message="response is missing the data envelope",
                request_id=resp.headers.get("X-Request-ID", ""),
            )
        return payload["data"]


class SyncTransport(BaseTransport):
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 2,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            store_io=store_io,
            media_expiration_seconds=media_expiration_seconds,
        )
        self._client = http_client or httpx.Client(timeout=timeout)

    def close(self) -> None:
        self._client.close()

    def request(self, method: str, path: str, *, json_body: Any = None, options: Optional[RequestOptions] = None) -> Any:
        attempt = 0
        while True:
            try:
                resp = self._client.request(
                    method, self.base_url + path, json=json_body, headers=self._headers(options)
                )
            except httpx.HTTPError as exc:
                if attempt < self.max_retries:
                    time.sleep(_backoff(attempt))
                    attempt += 1
                    continue
                raise APIConnectionError(f"veed: request failed: {exc}") from exc
            if resp.status_code < 300:
                return self._unwrap(resp)
            err = error_from_response(resp)
            if _retryable(resp.status_code) and attempt < self.max_retries:
                time.sleep(err.retry_after if err.retry_after else _backoff(attempt))
                attempt += 1
                continue
            raise err


class AsyncTransport(BaseTransport):
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 2,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            store_io=store_io,
            media_expiration_seconds=media_expiration_seconds,
        )
        self._client = http_client or httpx.AsyncClient(timeout=timeout)

    async def close(self) -> None:
        await self._client.aclose()

    async def request(
        self, method: str, path: str, *, json_body: Any = None, options: Optional[RequestOptions] = None
    ) -> Any:
        attempt = 0
        while True:
            try:
                resp = await self._client.request(
                    method, self.base_url + path, json=json_body, headers=self._headers(options)
                )
            except httpx.HTTPError as exc:
                if attempt < self.max_retries:
                    await asyncio.sleep(_backoff(attempt))
                    attempt += 1
                    continue
                raise APIConnectionError(f"veed: request failed: {exc}") from exc
            if resp.status_code < 300:
                return self._unwrap(resp)
            err = error_from_response(resp)
            if _retryable(resp.status_code) and attempt < self.max_retries:
                await asyncio.sleep(err.retry_after if err.retry_after else _backoff(attempt))
                attempt += 1
                continue
            raise err


def _inspect(job: Any, job_id: str) -> Optional[VeedError]:
    if job.status == "FAILED":
        error = getattr(job, "error", None)
        return JobFailedError(
            job_id=job_id,
            code=error.code if error else "",
            message=error.message if error else "",
            details=error.details if error else None,
            job=job,
        )
    if job.status == "CANCELLED":
        return JobCancelledError(job_id=job_id, job=job)
    return None


def wait_for_job(get_job: Callable[[], T], job_id: str, poll_interval: float, timeout: float) -> T:
    deadline = time.monotonic() + timeout
    last: Optional[T] = None
    while True:
        sleep_s = poll_interval
        try:
            job = get_job()
            last = job
            if job.status == "COMPLETED":  # type: ignore[attr-defined]
                return job
            terminal = _inspect(job, job_id)
            if terminal is not None:
                raise terminal
        except RateLimitError as exc:
            # The job keeps rendering server-side, so a rate-limited poll is
            # not fatal to the wait.
            sleep_s = exc.retry_after or poll_interval
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise WaitTimeoutError(job_id=job_id, timeout=timeout, job=last)
        # Or a poll answered with Retry-After decides the wait's real length.
        time.sleep(min(sleep_s, remaining))


async def async_wait_for_job(
    get_job: Callable[[], Awaitable[T]], job_id: str, poll_interval: float, timeout: float
) -> T:
    deadline = time.monotonic() + timeout
    last: Optional[T] = None
    while True:
        sleep_s = poll_interval
        try:
            job = await get_job()
            last = job
            if job.status == "COMPLETED":  # type: ignore[attr-defined]
                return job
            terminal = _inspect(job, job_id)
            if terminal is not None:
                raise terminal
        except RateLimitError as exc:
            sleep_s = exc.retry_after or poll_interval
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise WaitTimeoutError(job_id=job_id, timeout=timeout, job=last)
        await asyncio.sleep(min(sleep_s, remaining))
