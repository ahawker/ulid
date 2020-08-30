"""
    ulid/time
    ~~~~~~~~~

    Contains functionality for current time providers.
"""
import sys

from . import base, default, nanosecond

Provider = base.Provider

# Use :func:`~time.time_ns` when available for highest precision.
# See https://www.python.org/dev/peps/pep-0564/#annex-clocks-resolution-in-python for more details.
if sys.version_info >= (3, 7):
    PROVIDER = nanosecond.Provider()
else:
    PROVIDER = default.Provider()

milliseconds = PROVIDER.milliseconds
microseconds = PROVIDER.microseconds

__all__ = ['Provider', 'PROVIDER', 'milliseconds', 'microseconds']
