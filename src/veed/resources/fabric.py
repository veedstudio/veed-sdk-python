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

FabricResolution = Literal["720p", "480p"]
"""Output video resolution."""


class FabricJobErrorCode:
    """stable machine-readable failure codes for fabric-1.0 jobs. Kept as plain strings for forward compatibility."""

    INPUT_VALIDATION = "input_validation"
    CONTENT_MODERATION = "content_moderation"
    INVALID_FILE = "invalid_file"
    AUDIO_TOO_LONG = "audio_too_long"
    TRANSLOAD_FAILED = "transload_failed"
    GENERATION_FAILED = "generation_failed"
    TIMEOUT = "timeout"
    INSUFFICIENT_CREDITS = "insufficient_credits"


class FabricVideo(VeedModel):
    """The resource produced by a completed fabric-1.0 job."""

    video: File
    """Generated lip-synced video."""


class FabricJobError(VeedModel):
    """Why a fabric-1.0 job FAILED."""

    code: str
    message: str
    details: Optional[List[JobErrorDetail]] = None


class FabricJob(VeedModel):
    """The job envelope for the fabric-1.0 model."""

    job_id: str
    status: JobStatus
    result: Optional[FabricVideo] = None
    error: Optional[FabricJobError] = None


class Fabric:
    """Access to the fabric-1.0 model."""

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def submit(
        self,
        *,
        audio_url: str,
        image_url: str,
        resolution: FabricResolution,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> FabricJob:
        """Submit a fabric-1.0 job and return immediately (status PROCESSING)."""
        body = {
            "audio_url": audio_url,
            "image_url": image_url,
            "resolution": resolution,
        }
        data = self._transport.request(
            "POST",
            "/v1/fabric-1.0",
            json_body={k: v for k, v in body.items() if v is not None},
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return FabricJob.model_validate(data)

    def get(
        self,
        job_id: str,
        *,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> FabricJob:
        """Return one snapshot of a fabric-1.0 job."""
        data = self._transport.request(
            "GET",
            "/v1/fabric-1.0/" + quote(job_id, safe=""),
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return FabricJob.model_validate(data)

    def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 10,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> FabricJob:
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
        audio_url: str,
        image_url: str,
        resolution: FabricResolution,
        poll_interval: float = 10,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> FabricJob:
        """Submit a fabric-1.0 job and wait for the finished result."""
        job = self.submit(
            audio_url=audio_url,
            image_url=image_url,
            resolution=resolution,
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


class AsyncFabric:
    """Async access to the fabric-1.0 model."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def submit(
        self,
        *,
        audio_url: str,
        image_url: str,
        resolution: FabricResolution,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> FabricJob:
        """Submit a fabric-1.0 job and return immediately (status PROCESSING)."""
        body = {
            "audio_url": audio_url,
            "image_url": image_url,
            "resolution": resolution,
        }
        data = await self._transport.request(
            "POST",
            "/v1/fabric-1.0",
            json_body={k: v for k, v in body.items() if v is not None},
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return FabricJob.model_validate(data)

    async def get(
        self,
        job_id: str,
        *,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> FabricJob:
        """Return one snapshot of a fabric-1.0 job."""
        data = await self._transport.request(
            "GET",
            "/v1/fabric-1.0/" + quote(job_id, safe=""),
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return FabricJob.model_validate(data)

    async def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 10,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> FabricJob:
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
        audio_url: str,
        image_url: str,
        resolution: FabricResolution,
        poll_interval: float = 10,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> FabricJob:
        """Submit a fabric-1.0 job and wait for the finished result."""
        job = await self.submit(
            audio_url=audio_url,
            image_url=image_url,
            resolution=resolution,
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
