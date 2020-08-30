"""
    ulid/time/default
    ~~~~~~~~~~~~~~~~~

    Implements default time provider using :func:`~time.time`.
"""
import time

from ... import hints
from . import base


class Provider(base.Provider):
    """
    Returns time values from :func:`~time.time`.
    """
    def milliseconds(self) -> hints.Int:
        """
        Get the current time since unix epoch in milliseconds.

        :return: Epoch timestamp in milliseconds.
        :rtype: :class:`~int`
        """
        return int(time.time() * 1000)

    def microseconds(self) -> hints.Int:
        """
        Get the current time since unix epoch in microseconds.

        :return: Epoch timestamp in microseconds.
        :rtype: :class:`~int`
        """
        return int(time.time() * 1000 * 1000)
