"""
    ulid/time/base
    ~~~~~~~~~~~~~~

    Contains time abstract providers.
"""
import abc

from ... import hints


class Provider(metaclass=abc.ABCMeta):
    """
    Abstract class that defines providers for current time values.
    """
    @abc.abstractmethod
    def milliseconds(self) -> hints.Int:
        """
        Get the current time since unix epoch in milliseconds.

        :return: Epoch timestamp in milliseconds.
        :rtype: :class:`~int`
        """
        raise NotImplementedError('Method must be implemented by derived class')

    @abc.abstractmethod
    def microseconds(self) -> hints.Int:
        """
        Get the current time since unix epoch in microseconds.

        :return: Epoch timestamp in microseconds.
        :rtype: :class:`~int`
        """
        raise NotImplementedError('Method must be implemented by derived class')
