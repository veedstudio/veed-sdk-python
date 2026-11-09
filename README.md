# veed

Official Python SDK for the [VEED API](https://api.veed.io) — programmatic access to VEED's AI video models.

> Generated from VEED's OpenAPI spec. Do not edit by hand — changes are overwritten on the next release.

## Install

```bash
pip install veed
```

## Usage

```python
import veed

client = veed.Veed()  # reads VEED_API_KEY

# One-shot: submit and wait for the finished video.
job = client.fabric.generate(
    image_url="https://example.com/face.png",
    audio_url="https://example.com/speech.mp3",
    resolution="720p",
)
print(job.result.video.url)
```

Or keep control of the lifecycle:

```python
job = client.lipsync20.submit(
    video_url="https://example.com/source.mp4",
    audio_url="https://example.com/dub.mp3",
)
# ... persist job.job_id, come back later ...
job = client.lipsync20.wait(job.job_id, poll_interval=5.0, timeout=1800.0)
```

### Async

```python
async with veed.AsyncVeed() as client:
    job = await client.fabric.generate(
        image_url="https://example.com/face.png",
        audio_url="https://example.com/speech.mp3",
        resolution="720p",
    )
```

### Errors

HTTP-layer rejections raise subclasses of `veed.APIError` (with `.status_code`, `.code`,
`.request_id`). Accepted jobs that fail during rendering raise `veed.JobFailedError` from
`wait`/`generate`, with the model-specific failure code:

```python
try:
    job = client.fabric.generate(...)
except veed.JobFailedError as e:
    if e.code == veed.FabricJobErrorCode.CONTENT_MODERATION:
        ...  # handle moderation rejection
```

Retries (429/5xx, honoring `Retry-After`) are built in; submits are safe to retry because a
rejected submit never creates a job.

## Development

This SDK is generated, so fixes belong upstream rather than here — but to reproduce something
locally you need only [uv](https://docs.astral.sh/uv/), which fetches the interpreter pinned in
`.python-version` for you:

```bash
uv sync
uv run python -m unittest discover -s tests
```

## License

MIT — see [LICENSE](LICENSE).
