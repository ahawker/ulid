"""
    ulid/providers/default
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains data provider that creates new randomness values for the same timestamp.
"""
import os
import time

from .. import hints
from . import base


class Provider(base.Provider):
    """
    Provider that creates new randomness values for the same timestamp.
    """

    def timestamp(self) -> hints.Bytes:
        """
        Create a new timestamp value.

        :return: Timestamp value in bytes.
        :rtype: :class:`~bytes`
        """
        return int(time.time() * 1000).to_bytes(6, byteorder='big')

    def randomness(self, timestamp: hints.Bytes) -> hints.Bytes:
        """
        Create a new randomness value.

        :return: Randomness value in bytes.
        :rtype: :class:`~bytes`
        """
        return os.urandom(10)
