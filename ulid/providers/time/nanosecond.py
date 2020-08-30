"""
    ulid/time/time_ns
    ~~~~~~~~~~~~~~~~~

    Implements nanosecond time provider using :func:`~time.time_ns`.
"""
import time

from ... import hints
from . import base


class Provider(base.Provider):
    """
    Returns time values from :func:`~time.time_ns`.

    This class will only work on python 3.7+.
    """
    def milliseconds(self) -> hints.Int:
        """
        Get the current time since unix epoch in milliseconds.

        :return: Epoch timestamp in milliseconds.
        :rtype: :class:`~int`
        """
        return time.time_ns() // 1000000

    def microseconds(self) -> hints.Int:
        """
        Get the current time since unix epoch in microseconds.

        :return: Epoch timestamp in microseconds.
        :rtype: :class:`~int`
        """
        return time.time_ns() // 1000
