"""
    ulid/api
    ~~~~~~~~

    Defines the public API of the `ulid` package.
"""
import datetime
import os
import time
import uuid

from . import base32, hints, ulid


__all__ = ['new', 'from_bytes', 'from_int', 'from_str', 'from_uuid', 'from_timestamp', 'from_randomness']


def new() -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance.

    The timestamp is created from :func:`~time.time`.
    The randomness is created from :func:`~os.urandom`.

    :return: ULID from current timestamp
    :rtype: :class:`~ulid.ulid.ULID`
    """
    timestamp = int(time.time() * 1000).to_bytes(6, byteorder='big')
    randomness = os.urandom(10)
    return ulid.ULID(timestamp + randomness)


def from_bytes(value: hints.Buffer) -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance from the given :class:`~bytes`,
    :class:`~bytearray`, or :class:`~memoryview` value.

    :param value: 16 bytes
    :type value: :class:`~bytes`, :class:`~bytearray`, or :class:`~memoryview`
    :return: ULID from buffer value
    :rtype: :class:`~ulid.ulid.ULID`
    :raises ValueError: when the value is not 16 bytes
    """
    length = len(value)
    if length != 16:
        raise ValueError('Expects bytes to be 128 bits; got {} bytes'.format(length))

    return ulid.ULID(value)


def from_int(value: int) -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance from the given :class:`~int` value.

    :param value: 128 bit integer
    :type value: :class:`~int`
    :return: ULID from integer value
    :rtype: :class:`~ulid.ulid.ULID`
    :raises ValueError: when the value is not a 128 bit integer
    """
    length = (value.bit_length() + 7) // 8
    if length != 16:
        raise ValueError('Expects integer to be 128 bits; got {} bytes'.format(length))

    return ulid.ULID(value.to_bytes(16, byteorder='big'))


def from_str(value: str) -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance from the given :class:`~str` value.

    :param value: Base32 encoded string
    :type value: :class:`~str`
    :return: ULID from string value
    :rtype: :class:`~ulid.ulid.ULID`
    :raises ValueError: when the value is not 26 characters or malformed
    """
    return ulid.ULID(base32.decode_ulid(value))


def from_uuid(value: uuid.UUID) -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance from the given :class:`~uuid.UUID` value.

    :param value: UUIDv4 value
    :type value: :class:`~uuid.UUID`
    :return: ULID from UUID value
    :rtype: :class:`~ulid.ulid.ULID`
    """
    return ulid.ULID(value.bytes)


def from_timestamp(timestamp: hints.TimestampPrimitive) -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance using the given :class:`~int`, :class:`~float`,
    :class:`~str`, :class:`~bytes`, :class:`~bytearray`, or :class`~memoryview` value that
    represents Unix timestamp in seconds.

    :param timestamp: Unix timestamp in seconds
    :type timestamp: :class:`~int`, :class:`~float`, :class:`~str`,
        :class:`~bytes`, :class:`~bytearray`, :class:`~memoryview`, or :class:`~datetime.datetime`
    :return: ULID using given timestamp and new randomness
    :rtype: :class:`~ulid.ulid.ULID`
    :raises ValueError: when the value is an unsupported type
    :raises ValueError: when the value is a string and cannot be Base32 decoded
    :raises ValueError: when the value is or was converted to something 48 bits
    """
    if isinstance(timestamp, datetime.datetime):
        timestamp = timestamp.timestamp()
    if isinstance(timestamp, (int, float)):
        timestamp = int(timestamp * 1000.0).to_bytes(6, byteorder='big')
    elif isinstance(timestamp, str):
        timestamp = base32.decode_timestamp(timestamp)
    elif isinstance(timestamp, memoryview):
        timestamp = timestamp.tobytes()

    if not isinstance(timestamp, (bytes, bytearray)):
        raise ValueError('Expected int, float, str, bytes, '
                         'bytearray, or memoryview; got {}'.format(type(timestamp).__name__))

    length = len(timestamp)
    if length != 6:
        raise ValueError('Expects timestamp to be 48 bits; got {} bytes'.format(length))

    randomness = os.urandom(10)
    return ulid.ULID(timestamp + randomness)


def from_randomness(randomness: hints.RandomnessPrimitive) -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance using the given :class:`~int`, :class:`~float`,
    :class:`~str`, :class:`~bytes`, :class:`~bytearray`, or :class`~memoryview` value that
    represents cryptographically secure random values.

    :param randomness: Random bytes
    :type randomness: :class:`~int`, :class:`~float`, :class:`~str`,
        :class:`~bytes`, :class:`~bytearray`, or :class:`~memoryview`
    :return: ULID using new timestamp and given randomness
    :rtype: :class:`~ulid.ulid.ULID`
    :raises ValueError: when the value is an unsupported type
    :raises ValueError: when the value is a string and cannot be Base32 decoded
    :raises ValueError: when the value is or was converted to something 80 bits
    """
    if isinstance(randomness, (int, float)):
        randomness = int(randomness).to_bytes(10, byteorder='big')
    elif isinstance(randomness, str):
        randomness = base32.decode_randomness(randomness)
    elif isinstance(randomness, memoryview):
        randomness = randomness.tobytes()

    if not isinstance(randomness, (bytes, bytearray)):
        raise ValueError('Expected int, float, str, bytes, '
                         'bytearray, or memoryview; got {}'.format(type(randomness).__name__))

    length = len(randomness)
    if length != 10:
        raise ValueError('Expects randomness to be 80 bits; got {} bytes'.format(length))

    timestamp = int(time.time() * 1000).to_bytes(6, byteorder='big')
    return ulid.ULID(timestamp + randomness)
