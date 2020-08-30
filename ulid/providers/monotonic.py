"""
    ulid/providers/monotonic
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains data provider that monotonically increases randomness values for the same timestamp.
"""
import threading

from .. import consts, hints, ulid
from . import base


class Provider(base.Provider):
    """
    Provider that monotonically increases randomness values for the same timestamp.
    """
    def __init__(self, default: base.Provider):
        self.default = default
        self.lock = threading.Lock()
        self.prev_timestamp = consts.MIN_TIMESTAMP
        self.prev_randomness = consts.MIN_RANDOMNESS

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
        with self.lock:
            curr_timestamp = ulid.Timestamp(timestamp)

            # Randomness requested for new timestamp.
            if curr_timestamp > self.prev_timestamp:
                self.prev_randomness = ulid.Randomness(self.default.randomness(curr_timestamp.bytes))
                self.prev_timestamp = curr_timestamp

            # Randomness requested for same timestamp as previous request.
            else:
                if self.prev_randomness == consts.MAX_RANDOMNESS:
                    raise ValueError('Monotonic randomness value too large and will overflow')

                next_value = (self.prev_randomness.int + 1).to_bytes(10, byteorder='big')
                self.prev_randomness = ulid.Randomness(next_value)

        return self.prev_randomness.bytes
