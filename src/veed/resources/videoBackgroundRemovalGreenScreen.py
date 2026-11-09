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

from .videoBackgroundRemoval import VideoBackgroundRemovalJob
VideoBackgroundRemovalGreenScreenOutputCodec = Literal["vp9", "h264"]
"""Output encoding. vp9 (the default) yields a single webm video with an alpha channel; h264 yields two files (the RGB video and an alpha matte) and is recommended for better RGB quality."""



class VideoBackgroundRemovalGreenScreen:
    """Access to the video-background-removal-green-screen model."""

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def submit(
        self,
        *,
        output_codec: Optional[VideoBackgroundRemovalGreenScreenOutputCodec] = None,
        spill_suppression_strength: Optional[str] = None,
        video_url: str,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
        """Submit a video-background-removal-green-screen job and return immediately (status PROCESSING)."""
        body = {
            "output_codec": output_codec,
            "spill_suppression_strength": spill_suppression_strength,
            "video_url": video_url,
        }
        data = self._transport.request(
            "POST",
            "/v1/video-background-removal-green-screen",
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
        """Return one snapshot of a video-background-removal-green-screen job."""
        data = self._transport.request(
            "GET",
            "/v1/video-background-removal-green-screen/" + quote(job_id, safe=""),
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
        output_codec: Optional[VideoBackgroundRemovalGreenScreenOutputCodec] = None,
        spill_suppression_strength: Optional[str] = None,
        video_url: str,
        poll_interval: float = 10,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
        """Submit a video-background-removal-green-screen job and wait for the finished result."""
        job = self.submit(
            output_codec=output_codec,
            spill_suppression_strength=spill_suppression_strength,
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


class AsyncVideoBackgroundRemovalGreenScreen:
    """Async access to the video-background-removal-green-screen model."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def submit(
        self,
        *,
        output_codec: Optional[VideoBackgroundRemovalGreenScreenOutputCodec] = None,
        spill_suppression_strength: Optional[str] = None,
        video_url: str,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
        """Submit a video-background-removal-green-screen job and return immediately (status PROCESSING)."""
        body = {
            "output_codec": output_codec,
            "spill_suppression_strength": spill_suppression_strength,
            "video_url": video_url,
        }
        data = await self._transport.request(
            "POST",
            "/v1/video-background-removal-green-screen",
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
        """Return one snapshot of a video-background-removal-green-screen job."""
        data = await self._transport.request(
            "GET",
            "/v1/video-background-removal-green-screen/" + quote(job_id, safe=""),
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
        output_codec: Optional[VideoBackgroundRemovalGreenScreenOutputCodec] = None,
        spill_suppression_strength: Optional[str] = None,
        video_url: str,
        poll_interval: float = 10,
        timeout: float = DEFAULT_WAIT_TIMEOUT,
        store_io: Optional[bool] = None,
        media_expiration_seconds: Optional[int] = None,
    ) -> VideoBackgroundRemovalJob:
        """Submit a video-background-removal-green-screen job and wait for the finished result."""
        job = await self.submit(
            output_codec=output_codec,
            spill_suppression_strength=spill_suppression_strength,
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
