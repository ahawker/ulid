"""
    ulid/providers/provider
    ~~~~~~~~~~~~~~~~~~~~~~~

    Contains provider abstract classes.
"""
import abc

from .. import hints


class Provider(metaclass=abc.ABCMeta):
    """
    Abstract class that defines providers that yield timestamp and randomness values.
    """

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

        :return: Randomness value in bytes.
        :rtype: :class:`~bytes`
        """
        raise NotImplementedError('Method must be implemented by derived class')
