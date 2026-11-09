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

VideoBackgroundRemovalOutputCodec = Literal["vp9", "h264"]
"""Output encoding. vp9 (the default) yields a single webm video with an alpha channel; h264 yields two files (the RGB video and an alpha matte) and is recommended for better RGB quality."""


class VideoBackgroundRemovalJobErrorCode:
    """stable machine-readable failure codes for video-background-removal jobs. Kept as plain strings for forward compatibility."""

    INPUT_VALIDATION = "input_validation"
    CONTENT_MODERATION = "content_moderation"
    INVALID_FILE = "invalid_file"
    AUDIO_TOO_LONG = "audio_too_long"
    TRANSLOAD_FAILED = "transload_failed"
    GENERATION_FAILED = "generation_failed"
    TIMEOUT = "timeout"
    INSUFFICIENT_CREDITS = "insufficient_credits"


class VideoBackgroundRemovalFiles(VeedModel):
    """The resource produced by a completed video-background-removal job."""

    files: Optional[List[File]] = None
    """Rendered background-removed file(s): one webm with alpha for vp9; the RGB video and the alpha matte (two files) for h264."""


class VideoBackgroundRemovalJobError(VeedModel):
    """Why a video-background-removal job FAILED."""

    code: str
    message: str
    details: Optional[List[JobErrorDetail]] = None


class VideoBackgroundRemovalJob(VeedModel):
    """The job envelope for the video-background-removal model."""

    job_id: str
    status: JobStatus
    result: Optional[VideoBackgroundRemovalFiles] = None
    error: Optional[VideoBackgroundRemovalJobError] = None


class VideoBackgroundRemoval:
    """Access to the video-background-removal model."""

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def submit(
        self,
        *,
        output_codec: Optional[VideoBackgroundRemovalOutputCodec] = None,
        refine_foreground_edges: Optional[bool] = None,
        subject_is_person: Optional[bool] = None,
        video_url: str,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
        """Submit a video-background-removal job and return immediately (status PROCESSING)."""
        body = {
            "output_codec": output_codec,
            "refine_foreground_edges": refine_foreground_edges,
            "subject_is_person": subject_is_person,
            "video_url": video_url,
        }
        data = self._transport.request(
            "POST",
            "/v1/video-background-removal",
            json_body={k: v for k, v in body.items() if v is not None},
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return VideoBackgroundRemovalJob.model_validate(data)

    def get(
        self,
        job_id: str,
        *,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
        """Return one snapshot of a video-background-removal job."""
        data = self._transport.request(
            "GET",
            "/v1/video-background-removal/" + quote(job_id, safe=""),
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return VideoBackgroundRemovalJob.model_validate(data)

    def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 10,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
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
        output_codec: Optional[VideoBackgroundRemovalOutputCodec] = None,
        refine_foreground_edges: Optional[bool] = None,
        subject_is_person: Optional[bool] = None,
        video_url: str,
        poll_interval: float = 10,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
        """Submit a video-background-removal job and wait for the finished result."""
        job = self.submit(
            output_codec=output_codec,
            refine_foreground_edges=refine_foreground_edges,
            subject_is_person=subject_is_person,
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


class AsyncVideoBackgroundRemoval:
    """Async access to the video-background-removal model."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def submit(
        self,
        *,
        output_codec: Optional[VideoBackgroundRemovalOutputCodec] = None,
        refine_foreground_edges: Optional[bool] = None,
        subject_is_person: Optional[bool] = None,
        video_url: str,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
        """Submit a video-background-removal job and return immediately (status PROCESSING)."""
        body = {
            "output_codec": output_codec,
            "refine_foreground_edges": refine_foreground_edges,
            "subject_is_person": subject_is_person,
            "video_url": video_url,
        }
        data = await self._transport.request(
            "POST",
            "/v1/video-background-removal",
            json_body={k: v for k, v in body.items() if v is not None},
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return VideoBackgroundRemovalJob.model_validate(data)

    async def get(
        self,
        job_id: str,
        *,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
        """Return one snapshot of a video-background-removal job."""
        data = await self._transport.request(
            "GET",
            "/v1/video-background-removal/" + quote(job_id, safe=""),
            options=RequestOptions(store_io=store_io, media_expiration_seconds=media_expiration_seconds),
        )
        return VideoBackgroundRemovalJob.model_validate(data)

    async def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 10,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
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
        output_codec: Optional[VideoBackgroundRemovalOutputCodec] = None,
        refine_foreground_edges: Optional[bool] = None,
        subject_is_person: Optional[bool] = None,
        video_url: str,
        poll_interval: float = 10,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
        """Submit a video-background-removal job and wait for the finished result."""
        job = await self.submit(
            output_codec=output_codec,
            refine_foreground_edges=refine_foreground_edges,
            subject_is_person=subject_is_person,
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
