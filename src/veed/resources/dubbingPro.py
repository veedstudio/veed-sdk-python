# Code generated from the VEED OpenAPI spec. DO NOT EDIT.

from __future__ import annotations

from typing import List, Literal, Optional
from urllib.parse import quote

from .._transport import (
    DEFAULT_WAIT_TIMEOUT,
    AsyncTransport,
    RequestOptions,
    SyncTransport,
    async_wait_for_job,
    wait_for_job,
)
from .._types import File, JobErrorDetail, JobStatus, VeedModel

from .dubbing import DubbingJob


class DubbingPro:
    """Access to the dubbing-pro model."""

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def submit(
        self,
        *,
        source_language: Optional[str] = None,
        target_language: str,
        video_url: str,
        voice_cloning_strength: Optional[int] = None,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> DubbingJob:
        """Submit a dubbing-pro job and return immediately (status PROCESSING)."""
        body = {
            "source_language": source_language,
            "target_language": target_language,
            "video_url": video_url,
            "voice_cloning_strength": voice_cloning_strength,
        }
        data = self._transport.request(
            "POST",
            "/v1/dubbing-pro",
            json_body={k: v for k, v in body.items() if v is not None},
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return DubbingJob.model_validate(data)

    def get(
        self,
        job_id: str,
        *,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> DubbingJob:
        """Return one snapshot of a dubbing-pro job."""
        data = self._transport.request(
            "GET",
            "/v1/dubbing-pro/" + quote(job_id, safe=""),
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return DubbingJob.model_validate(data)

    def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> DubbingJob:
        """Poll until the job reaches a terminal state.

        Returns the COMPLETED job; raises JobFailedError, JobCancelledError or
        WaitTimeoutError otherwise (each carries the last-seen job).
        """
        return wait_for_job(
            lambda: self.get(job_id, store_io=store_io, media_expiration_seconds=media_expiration_seconds),
            job_id,
            poll_interval,
            timeout,
        )

    def generate(
        self,
        *,
        source_language: Optional[str] = None,
        target_language: str,
        video_url: str,
        voice_cloning_strength: Optional[int] = None,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> DubbingJob:
        """Submit a dubbing-pro job and wait for the finished result."""
        job = self.submit(
            source_language=source_language,
            target_language=target_language,
            video_url=video_url,
            voice_cloning_strength=voice_cloning_strength,
            store_io=store_io,
            media_expiration_seconds=media_expiration_seconds,
        )
        return self.wait(
            job.job_id,
            poll_interval=poll_interval,
            timeout=timeout,
            store_io=store_io,
            media_expiration_seconds=media_expiration_seconds,
        )


class AsyncDubbingPro:
    """Async access to the dubbing-pro model."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def submit(
        self,
        *,
        source_language: Optional[str] = None,
        target_language: str,
        video_url: str,
        voice_cloning_strength: Optional[int] = None,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> DubbingJob:
        """Submit a dubbing-pro job and return immediately (status PROCESSING)."""
        body = {
            "source_language": source_language,
            "target_language": target_language,
            "video_url": video_url,
            "voice_cloning_strength": voice_cloning_strength,
        }
        data = await self._transport.request(
            "POST",
            "/v1/dubbing-pro",
            json_body={k: v for k, v in body.items() if v is not None},
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return DubbingJob.model_validate(data)

    async def get(
        self,
        job_id: str,
        *,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> DubbingJob:
        """Return one snapshot of a dubbing-pro job."""
        data = await self._transport.request(
            "GET",
            "/v1/dubbing-pro/" + quote(job_id, safe=""),
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return DubbingJob.model_validate(data)

    async def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> DubbingJob:
        """Poll until the job reaches a terminal state.

        Returns the COMPLETED job; raises JobFailedError, JobCancelledError or
        WaitTimeoutError otherwise (each carries the last-seen job).
        """
        return await async_wait_for_job(
            lambda: self.get(job_id, store_io=store_io, media_expiration_seconds=media_expiration_seconds),
            job_id,
            poll_interval,
            timeout,
        )

    async def generate(
        self,
        *,
        source_language: Optional[str] = None,
        target_language: str,
        video_url: str,
        voice_cloning_strength: Optional[int] = None,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> DubbingJob:
        """Submit a dubbing-pro job and wait for the finished result."""
        job = await self.submit(
            source_language=source_language,
            target_language=target_language,
            video_url=video_url,
            voice_cloning_strength=voice_cloning_strength,
            store_io=store_io,
            media_expiration_seconds=media_expiration_seconds,
        )
        return await self.wait(
            job.job_id,
            poll_interval=poll_interval,
            timeout=timeout,
            store_io=store_io,
            media_expiration_seconds=media_expiration_seconds,
        )
