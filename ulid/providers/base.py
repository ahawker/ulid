"""
    ulid/providers/provider
    ~~~~~~~~~~~~~~~~~~~~~~~

    Contains provider abstract classes.
"""
import abc
import typing

from .. import hints

#: Type hint that defines a two item tuple of bytes returned by the provider.
TimestampRandomnessBytes = typing.Tuple[hints.Bytes, hints.Bytes]  # pylint: disable=invalid-name


class Provider(metaclass=abc.ABCMeta):
    """
    Abstract class that defines providers that yield timestamp and randomness values.
    """
    def new(self) -> TimestampRandomnessBytes:
        """
        Create a new timestamp and randomness value.

        :return: Two item tuple containing timestamp and randomness values as :class:`~bytes`.
        :rtype: :class:`~tuple`
        """
        timestamp = self.timestamp()
        randomness = self.randomness(timestamp)
        return timestamp, randomness

    @abc.abstractmethod
    def timestamp(self) -> hints.Bytes:
        """
        Create a new timestamp value.

        :return: Timestamp value in bytes.
        :rtype: :class:`~bytes`
        """
        raise NotImplementedError('Method must be implemented by derived class')

    @abc.abstractmethod
    def randomness(self, timestamp: hints.Bytes) -> hints.Bytes:
        """
        Create a new randomness value.

        :param timestamp: Timestamp in milliseconds
        :type timestamp: :class:`~bytes`
        :return: Randomness value in bytes.
        :rtype: :class:`~bytes`
        """
        raise NotImplementedError('Method must be implemented by derived class')
