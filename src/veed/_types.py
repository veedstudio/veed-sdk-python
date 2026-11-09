# Code generated from the VEED OpenAPI spec. DO NOT EDIT.

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict

# Kept as str (not an Enum/Literal) so a new server-side status never breaks
# deserialization in old SDK versions.
JobStatus = str

JOB_STATUS_PROCESSING = "PROCESSING"
JOB_STATUS_COMPLETED = "COMPLETED"
JOB_STATUS_FAILED = "FAILED"
JOB_STATUS_CANCELLED = "CANCELLED"


class VeedModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class File(VeedModel):
    """A downloadable media file produced by a job."""

    url: str
    content_type: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None


class JobErrorDetail(VeedModel):
    """One structured entry of a job-level failure."""

    type: str
    message: str
    field: Optional[str] = None
