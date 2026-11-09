# Code generated from the VEED OpenAPI spec. DO NOT EDIT.

from __future__ import annotations

from typing import Optional

import httpx

from ._transport import AsyncTransport, SyncTransport
from .resources import (
    AsyncCleanAudio,
    CleanAudio,
    AsyncCleanAudioVideo,
    CleanAudioVideo,
    AsyncDubbing,
    Dubbing,
    AsyncDubbingPro,
    DubbingPro,
    AsyncFabric,
    Fabric,
    AsyncLipsync20,
    Lipsync20,
    AsyncVideoBackgroundRemoval,
    VideoBackgroundRemoval,
    AsyncVideoBackgroundRemovalFast,
    VideoBackgroundRemovalFast,
    AsyncVideoBackgroundRemovalGreenScreen,
    VideoBackgroundRemovalGreenScreen,
)


class Veed:
    """VEED API client. Construct once with your API key and reuse; safe to
    share across threads.

        client = veed.Veed()  # reads VEED_API_KEY
    """

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
        self._transport = SyncTransport(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            store_io=store_io,
            media_expiration_seconds=media_expiration_seconds,
            http_client=http_client,
        )
        self.cleanAudio = CleanAudio(self._transport)
        self.cleanAudioVideo = CleanAudioVideo(self._transport)
        self.dubbing = Dubbing(self._transport)
        self.dubbingPro = DubbingPro(self._transport)
        self.fabric = Fabric(self._transport)
        self.lipsync20 = Lipsync20(self._transport)
        self.videoBackgroundRemoval = VideoBackgroundRemoval(self._transport)
        self.videoBackgroundRemovalFast = VideoBackgroundRemovalFast(self._transport)
        self.videoBackgroundRemovalGreenScreen = VideoBackgroundRemovalGreenScreen(self._transport)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> "Veed":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


class AsyncVeed:
    """Async VEED API client (asyncio + httpx.AsyncClient)."""

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
        self._transport = AsyncTransport(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            store_io=store_io,
            media_expiration_seconds=media_expiration_seconds,
            http_client=http_client,
        )
        self.cleanAudio = AsyncCleanAudio(self._transport)
        self.cleanAudioVideo = AsyncCleanAudioVideo(self._transport)
        self.dubbing = AsyncDubbing(self._transport)
        self.dubbingPro = AsyncDubbingPro(self._transport)
        self.fabric = AsyncFabric(self._transport)
        self.lipsync20 = AsyncLipsync20(self._transport)
        self.videoBackgroundRemoval = AsyncVideoBackgroundRemoval(self._transport)
        self.videoBackgroundRemovalFast = AsyncVideoBackgroundRemovalFast(self._transport)
        self.videoBackgroundRemovalGreenScreen = AsyncVideoBackgroundRemovalGreenScreen(self._transport)

    async def close(self) -> None:
        await self._transport.close()

    async def __aenter__(self) -> "AsyncVeed":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.close()
