"""
This file has been modified by NetworktoCode, LLC.
"""
from pkg_resources import get_distribution, DistributionNotFound

from pynautobot.core.query import RequestError, AllocationError, ContentError
from pynautobot.core.api import Api as api


__all__ = ["RequestError", "AllocationError", "ContentError", "api"]

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass
