# Code generated from the VEED OpenAPI spec. DO NOT EDIT.

from ._errors import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    InternalServerError,
    InvalidRequestError,
    JobCancelledError,
    JobFailedError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    VeedError,
    WaitTimeoutError,
)
from ._types import (
    JOB_STATUS_CANCELLED,
    JOB_STATUS_COMPLETED,
    JOB_STATUS_FAILED,
    JOB_STATUS_PROCESSING,
    File,
    JobErrorDetail,
    JobStatus,
)
from ._version import VERSION
from .client import AsyncVeed, Veed
from .resources.cleanAudio import (
    AsyncCleanAudio,
    CleanAudio,
    CleanAudioJob,
    CleanAudioJobError,
    CleanAudioJobErrorCode,
    CleanAudio,
    CleanAudioOutputFormat,
)
from .resources.cleanAudioVideo import (
    AsyncCleanAudioVideo,
    CleanAudioVideo,
    CleanAudioVideoJob,
    CleanAudioVideo,
)
from .resources.dubbing import (
    AsyncDubbing,
    Dubbing,
    DubbingJob,
    DubbingJobError,
    DubbingJobErrorCode,
    Dubbing,
)
from .resources.dubbingPro import (
    AsyncDubbingPro,
    DubbingPro,
)
from .resources.fabric import (
    AsyncFabric,
    Fabric,
    FabricJob,
    FabricJobError,
    FabricJobErrorCode,
    FabricVideo,
    FabricResolution,
)
from .resources.lipsync20 import (
    AsyncLipsync20,
    Lipsync20,
    Lipsync20Job,
    Lipsync20JobError,
    Lipsync20JobErrorCode,
    Lipsync20Video,
)
from .resources.videoBackgroundRemoval import (
    AsyncVideoBackgroundRemoval,
    VideoBackgroundRemoval,
    VideoBackgroundRemovalJob,
    VideoBackgroundRemovalJobError,
    VideoBackgroundRemovalJobErrorCode,
    VideoBackgroundRemovalFiles,
    VideoBackgroundRemovalOutputCodec,
)
from .resources.videoBackgroundRemovalFast import (
    AsyncVideoBackgroundRemovalFast,
    VideoBackgroundRemovalFast,
    VideoBackgroundRemovalFastOutputCodec,
)
from .resources.videoBackgroundRemovalGreenScreen import (
    AsyncVideoBackgroundRemovalGreenScreen,
    VideoBackgroundRemovalGreenScreen,
    VideoBackgroundRemovalGreenScreenOutputCodec,
)

__version__ = VERSION
