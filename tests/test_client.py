# Code generated from the VEED OpenAPI spec. DO NOT EDIT.

import asyncio
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from veed import (
    AsyncVeed,
    JobFailedError,
    NotFoundError,
    RateLimitError,
    Veed,
    WaitTimeoutError,
)
from veed._errors import MAX_RETRY_AFTER


def make_server(router):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _handle(self):
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b""
            status, payload, headers = router(self.command, self.path, body, self.headers)
            data = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            for k, v in (headers or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)

        do_GET = _handle
        do_POST = _handle

    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, "http://127.0.0.1:%d" % srv.server_port


PROCESSING = {"data": {"job_id": "j1", "status": "PROCESSING"}}
COMPLETED = {
    "data": {
        "job_id": "j1",
        "status": "COMPLETED",
        "result": {"video": {"url": "https://cdn/out.mp4"}},
    }
}


class ClientTest(unittest.TestCase):
    def start(self, router):
        srv, url = make_server(router)
        self.addCleanup(srv.shutdown)
        return url

    def test_generate_end_to_end(self):
        seen = {"gets": 0, "auth": None}

        def router(method, path, body, headers):
            if method == "POST" and path == "/v1/fabric-1.0":
                seen["auth"] = headers.get("Authorization")
                parsed = json.loads(body)
                self.assertEqual(parsed["resolution"], "720p")
                return 202, PROCESSING, None
            self.assertEqual(path, "/v1/fabric-1.0/j1")
            seen["gets"] += 1
            return 200, (PROCESSING if seen["gets"] < 2 else COMPLETED), None

        client = Veed(api_key="vp_test", base_url=self.start(router))
        job = client.fabric.generate(
            image_url="https://in/i.png",
            audio_url="https://in/a.mp3",
            resolution="720p",
            poll_interval=0.001,
        )
        self.assertEqual(job.result.video.url, "https://cdn/out.mp4")
        self.assertEqual(seen["auth"], "Bearer vp_test")

    def test_error_mapping(self):
        def router(method, path, body, headers):
            return 404, {"error": {"code": "not_found", "message": "no such job", "request_id": "req-1"}}, None

        client = Veed(api_key="vp_test", base_url=self.start(router))
        with self.assertRaises(NotFoundError) as ctx:
            client.fabric.get("missing")
        self.assertEqual(ctx.exception.code, "not_found")
        self.assertEqual(ctx.exception.request_id, "req-1")

    def test_job_failed(self):
        failed = {
            "data": {
                "job_id": "j1",
                "status": "FAILED",
                "error": {"code": "content_moderation", "message": "rejected"},
            }
        }

        def router(method, path, body, headers):
            return 200, failed, None

        client = Veed(api_key="vp_test", base_url=self.start(router))
        with self.assertRaises(JobFailedError) as ctx:
            client.fabric.wait("j1", poll_interval=0.001)
        self.assertEqual(ctx.exception.code, "content_moderation")
        self.assertEqual(ctx.exception.job.status, "FAILED")

    def test_wait_timeout(self):
        def router(method, path, body, headers):
            return 200, PROCESSING, None

        client = Veed(api_key="vp_test", base_url=self.start(router))
        with self.assertRaises(WaitTimeoutError):
            client.fabric.wait("j1", poll_interval=0.001, timeout=0.01)

    def test_retry_after_on_429(self):
        seen = {"calls": 0}

        def router(method, path, body, headers):
            seen["calls"] += 1
            if seen["calls"] == 1:
                return (
                    429,
                    {"error": {"code": "rate_limited", "message": "slow down", "request_id": "r"}},
                    {"Retry-After": "0"},
                )
            return 202, {"data": {"job_id": "j9", "status": "PROCESSING"}}, None

        client = Veed(api_key="vp_test", base_url=self.start(router))
        job = client.lipsync20.submit(video_url="https://in/v.mp4", audio_url="https://in/a.mp3")
        self.assertEqual(job.job_id, "j9")
        self.assertEqual(seen["calls"], 2)

    def test_client_default_headers_and_override(self):
        seen = {}

        def router(method, path, body, headers):
            seen["store"] = headers.get("X-Veed-Store-IO")
            seen["media"] = headers.get("X-Veed-Media-Expiration-Seconds")
            return 200, PROCESSING, None

        client = Veed(
            api_key="vp_test",
            base_url=self.start(router),
            store_io=False,
            media_expiration_seconds=600,
        )
        client.fabric.get("j1")
        self.assertEqual(seen["store"], "0")
        self.assertEqual(seen["media"], "600")

        client.fabric.get("j1", store_io=True, media_expiration_seconds=60)
        self.assertEqual(seen["store"], "1")
        self.assertEqual(seen["media"], "60")

    def test_async_generate(self):
        seen = {"gets": 0}

        def router(method, path, body, headers):
            if method == "POST":
                return 202, PROCESSING, None
            seen["gets"] += 1
            return 200, (PROCESSING if seen["gets"] < 2 else COMPLETED), None

        url = self.start(router)

        async def run():
            async with AsyncVeed(api_key="vp_test", base_url=url) as client:
                return await client.fabric.generate(
                    image_url="https://in/i.png",
                    audio_url="https://in/a.mp3",
                    resolution="720p",
                    poll_interval=0.001,
                )

        job = asyncio.run(run())
        self.assertEqual(job.result.video.url, "https://cdn/out.mp4")

    # Retry-After: 0 fails the truthiness guard every caller applies, so the
    # suite left the parser unexercised.
    def test_retry_after_is_clamped(self):
        def router(method, path, body, headers):
            return (
                429,
                {"error": {"code": "rate_limited", "message": "slow down", "request_id": "r"}},
                {"Retry-After": "999999999"},
            )

        client = Veed(api_key="vp_test", base_url=self.start(router), max_retries=0)
        with self.assertRaises(RateLimitError) as caught:
            client.fabric.get("j1")
        self.assertEqual(caught.exception.retry_after, MAX_RETRY_AFTER)

    def test_wait_timeout_survives_retry_after(self):
        def router(method, path, body, headers):
            return (
                429,
                {"error": {"code": "rate_limited", "message": "slow down", "request_id": "r"}},
                {"Retry-After": "600"},
            )

        client = Veed(api_key="vp_test", base_url=self.start(router), max_retries=0)
        with self.assertRaises(WaitTimeoutError):
            client.fabric.wait("j1", poll_interval=0.001, timeout=0.01)


if __name__ == "__main__":
    unittest.main()
