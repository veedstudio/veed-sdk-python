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

CleanAudioOutputFormat = Literal["flac", "wav"]
"""Container for the 48 kHz mono 16-bit output. FLAC is lossless at about half the size of WAV."""


class CleanAudioJobErrorCode:
    """stable machine-readable failure codes for clean-audio jobs. Kept as plain strings for forward compatibility."""

    INPUT_VALIDATION = "input_validation"
    CONTENT_MODERATION = "content_moderation"
    INVALID_FILE = "invalid_file"
    AUDIO_TOO_LONG = "audio_too_long"
    TRANSLOAD_FAILED = "transload_failed"
    GENERATION_FAILED = "generation_failed"
    TIMEOUT = "timeout"
    INSUFFICIENT_CREDITS = "insufficient_credits"


class CleanAudio(VeedModel):
    """The resource produced by a completed clean-audio job."""

    audio: File
    """The denoised recording: 48 kHz mono, the same duration as the input."""


class CleanAudioJobError(VeedModel):
    """Why a clean-audio job FAILED."""

    code: str
    message: str
    details: Optional[List[JobErrorDetail]] = None


class CleanAudioJob(VeedModel):
    """The job envelope for the clean-audio model."""

    job_id: str
    status: JobStatus
    result: Optional[CleanAudio] = None
    error: Optional[CleanAudioJobError] = None


class CleanAudio:
    """Access to the clean-audio model."""

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def submit(
        self,
        *,
        audio_url: str,
        normalize_loudness: Optional[bool] = None,
        output_format: Optional[CleanAudioOutputFormat] = None,
        strength: Optional[str] = None,
        target_lufs: Optional[str] = None,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioJob:
        """Submit a clean-audio job and return immediately (status PROCESSING)."""
        body = {
            "audio_url": audio_url,
            "normalize_loudness": normalize_loudness,
            "output_format": output_format,
            "strength": strength,
            "target_lufs": target_lufs,
        }
        data = self._transport.request(
            "POST",
            "/v1/clean-audio",
            json_body={k: v for k, v in body.items() if v is not None},
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return CleanAudioJob.model_validate(data)

    def get(
        self,
        job_id: str,
        *,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioJob:
        """Return one snapshot of a clean-audio job."""
        data = self._transport.request(
            "GET",
            "/v1/clean-audio/" + quote(job_id, safe=""),
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return CleanAudioJob.model_validate(data)

    def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioJob:
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
        normalize_loudness: Optional[bool] = None,
        output_format: Optional[CleanAudioOutputFormat] = None,
        strength: Optional[str] = None,
        target_lufs: Optional[str] = None,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioJob:
        """Submit a clean-audio job and wait for the finished result."""
        job = self.submit(
            audio_url=audio_url,
            normalize_loudness=normalize_loudness,
            output_format=output_format,
            strength=strength,
            target_lufs=target_lufs,
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


class AsyncCleanAudio:
    """Async access to the clean-audio model."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def submit(
        self,
        *,
        audio_url: str,
        normalize_loudness: Optional[bool] = None,
        output_format: Optional[CleanAudioOutputFormat] = None,
        strength: Optional[str] = None,
        target_lufs: Optional[str] = None,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioJob:
        """Submit a clean-audio job and return immediately (status PROCESSING)."""
        body = {
            "audio_url": audio_url,
            "normalize_loudness": normalize_loudness,
            "output_format": output_format,
            "strength": strength,
            "target_lufs": target_lufs,
        }
        data = await self._transport.request(
            "POST",
            "/v1/clean-audio",
            json_body={k: v for k, v in body.items() if v is not None},
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return CleanAudioJob.model_validate(data)

    async def get(
        self,
        job_id: str,
        *,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioJob:
        """Return one snapshot of a clean-audio job."""
        data = await self._transport.request(
            "GET",
            "/v1/clean-audio/" + quote(job_id, safe=""),
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return CleanAudioJob.model_validate(data)

    async def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioJob:
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
        normalize_loudness: Optional[bool] = None,
        output_format: Optional[CleanAudioOutputFormat] = None,
        strength: Optional[str] = None,
        target_lufs: Optional[str] = None,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioJob:
        """Submit a clean-audio job and wait for the finished result."""
        job = await self.submit(
            audio_url=audio_url,
            normalize_loudness=normalize_loudness,
            output_format=output_format,
            strength=strength,
            target_lufs=target_lufs,
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
