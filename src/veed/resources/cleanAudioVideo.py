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

from .cleanAudio import CleanAudioJobError


class CleanAudioVideo(VeedModel):
    """The resource produced by a completed clean-audio-video job."""

    video: File
    """The input video with its audio track replaced by the denoised one. The picture is copied unchanged; the audio is 48 kHz mono, AAC in an MP4 for H.264, HEVC, AV1 or MPEG-4 input, Opus in a WebM for VP8 or VP9."""


class CleanAudioVideoJob(VeedModel):
    """The job envelope for the clean-audio-video model."""

    job_id: str
    status: JobStatus
    result: Optional[CleanAudioVideo] = None
    error: Optional[CleanAudioJobError] = None


class CleanAudioVideo:
    """Access to the clean-audio-video model."""

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def submit(
        self,
        *,
        normalize_loudness: Optional[bool] = None,
        strength: Optional[str] = None,
        target_lufs: Optional[str] = None,
        video_url: str,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioVideoJob:
        """Submit a clean-audio-video job and return immediately (status PROCESSING)."""
        body = {
            "normalize_loudness": normalize_loudness,
            "strength": strength,
            "target_lufs": target_lufs,
            "video_url": video_url,
        }
        data = self._transport.request(
            "POST",
            "/v1/clean-audio-video",
            json_body={k: v for k, v in body.items() if v is not None},
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return CleanAudioVideoJob.model_validate(data)

    def get(
        self,
        job_id: str,
        *,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioVideoJob:
        """Return one snapshot of a clean-audio-video job."""
        data = self._transport.request(
            "GET",
            "/v1/clean-audio-video/" + quote(job_id, safe=""),
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return CleanAudioVideoJob.model_validate(data)

    def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioVideoJob:
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
        normalize_loudness: Optional[bool] = None,
        strength: Optional[str] = None,
        target_lufs: Optional[str] = None,
        video_url: str,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioVideoJob:
        """Submit a clean-audio-video job and wait for the finished result."""
        job = self.submit(
            normalize_loudness=normalize_loudness,
            strength=strength,
            target_lufs=target_lufs,
            video_url=video_url,
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


class AsyncCleanAudioVideo:
    """Async access to the clean-audio-video model."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def submit(
        self,
        *,
        normalize_loudness: Optional[bool] = None,
        strength: Optional[str] = None,
        target_lufs: Optional[str] = None,
        video_url: str,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioVideoJob:
        """Submit a clean-audio-video job and return immediately (status PROCESSING)."""
        body = {
            "normalize_loudness": normalize_loudness,
            "strength": strength,
            "target_lufs": target_lufs,
            "video_url": video_url,
        }
        data = await self._transport.request(
            "POST",
            "/v1/clean-audio-video",
            json_body={k: v for k, v in body.items() if v is not None},
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return CleanAudioVideoJob.model_validate(data)

    async def get(
        self,
        job_id: str,
        *,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioVideoJob:
        """Return one snapshot of a clean-audio-video job."""
        data = await self._transport.request(
            "GET",
            "/v1/clean-audio-video/" + quote(job_id, safe=""),
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return CleanAudioVideoJob.model_validate(data)

    async def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioVideoJob:
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
        normalize_loudness: Optional[bool] = None,
        strength: Optional[str] = None,
        target_lufs: Optional[str] = None,
        video_url: str,
        poll_interval: float = 15,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> CleanAudioVideoJob:
        """Submit a clean-audio-video job and wait for the finished result."""
        job = await self.submit(
            normalize_loudness=normalize_loudness,
            strength=strength,
            target_lufs=target_lufs,
            video_url=video_url,
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
