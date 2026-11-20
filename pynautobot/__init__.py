"""This file has been modified by NetworktoCode, LLC."""

from importlib.metadata import PackageNotFoundError, version

from pynautobot.core.api import Api as api
from pynautobot.core.query import AllocationError, ContentError, RequestError, RetriesExhaustedError
from pynautobot.core.rate_limit import RateLimit

__all__ = [
    "RequestError",
    "RetriesExhaustedError",
    "AllocationError",
    "ContentError",
    "RateLimit",
    "api",
    "__version__",
]


try:
    __version__ = version(__package__)
except PackageNotFoundError:
    __version__ = "Unable to determine version; no package found"
