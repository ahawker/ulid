"""
    ulid/providers/microsecond
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains data provider that uses precise timestamp and most significant randomness bits.
"""
import os
import sys

from .. import hints
from . import base, time


class Provider(base.Provider):
    """
    Provider that uses microsecond values for timestamp and most significant randomness bits.
    """
    def __init__(self, default: base.Provider):
        self.default = default

    def new(self) -> base.TimestampRandomnessBytes:
        """
        Create a new timestamp and randomness value.

        :return: Two item tuple containing timestamp and randomness values as :class:`~bytes`.
        :rtype: :class:`~tuple`
        """
        epoch_us = time.microseconds()
        epoch_ms = epoch_us // 1000
        microseconds = epoch_us % epoch_ms

        # Microsecond will be 0-1000 so we only need 10-bits to store it. Build a prefix
        # from those 10-bits and a random 6-bits to use our two bytes completely.
        microseconds_bits = microseconds << 6
        randomness_bits = int.from_bytes(os.urandom(1), sys.byteorder) & 63
        randomness_prefix = (microseconds_bits | randomness_bits).to_bytes(2, byteorder='big')

        timestamp = epoch_ms.to_bytes(6, byteorder='big')
        randomness = randomness_prefix + os.urandom(8)

        return timestamp, randomness

    def timestamp(self) -> hints.Bytes:
        """
        Create a new timestamp value.

        :return: Timestamp value in bytes.
        :rtype: :class:`~bytes`
        """
        return self.default.timestamp()

    def randomness(self, timestamp: hints.Bytes) -> hints.Bytes:
        """
        Create a new randomness value.

        :param timestamp: Timestamp in milliseconds
        :type timestamp: :class:`~bytes`
        :return: Randomness value in bytes.
        :rtype: :class:`~bytes`
        """
        return self.default.randomness(timestamp)
