"""
    ulid/api
    ~~~~~~~~

    Defines the public API of the `ulid` package.
"""
import os
import time
import typing
import uuid

from . import base32, codec, hints, ulid

__all__ = ['new', 'parse', 'create', 'from_bytes', 'from_int', 'from_str',
           'from_uuid', 'from_timestamp', 'from_randomness',
           'MIN_TIMESTAMP', 'MAX_TIMESTAMP', 'MIN_RANDOMNESS', 'MAX_RANDOMNESS', 'MIN_ULID', 'MAX_ULID']

#: Minimum possible timestamp value (0).
MIN_TIMESTAMP = ulid.Timestamp(b'\x00\x00\x00\x00\x00\x00')


#: Maximum possible timestamp value (281474976710.655 epoch).
MAX_TIMESTAMP = ulid.Timestamp(b'\xff\xff\xff\xff\xff\xff')


#: Minimum possible randomness value (0).
MIN_RANDOMNESS = ulid.Randomness(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')


#: Maximum possible randomness value (1208925819614629174706175).
MAX_RANDOMNESS = ulid.Randomness(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')


#: Minimum possible ULID value (0).
MIN_ULID = ulid.ULID(MIN_TIMESTAMP.bytes + MIN_RANDOMNESS.bytes)


#: Maximum possible ULID value (340282366920938463463374607431768211455).
MAX_ULID = ulid.ULID(MAX_TIMESTAMP.bytes + MAX_RANDOMNESS.bytes)


#: Type hint that defines multiple primitive types that can represent a full ULID.
ULIDPrimitive = typing.Union[hints.Primitive, uuid.UUID, ulid.ULID]  # pylint: disable=invalid-name


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


def parse(value: ULIDPrimitive) -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance from the given value.

    .. note:: This method should only be used when the caller is trying to parse a ULID from
    a value when they're unsure what format/primitive type it will be given in.

    :param value: ULID value of any supported type
    :type value: :class:`~ulid.api.ULIDPrimitive`
    :return: ULID from value
    :rtype: :class:`~ulid.ulid.ULID`
    :raises ValueError: when unable to parse a ULID from the value
    """
    if isinstance(value, ulid.ULID):
        return value
    if isinstance(value, uuid.UUID):
        return from_uuid(value)
    if isinstance(value, str):
        len_value = len(value)
        if len_value == 36:
            return from_uuid(uuid.UUID(value))
        if len_value == 32:
            return from_uuid(uuid.UUID(value))
        if len_value == 26:
            return from_str(value)
        if len_value == 16:
            return from_randomness(value)
        if len_value == 10:
            return from_timestamp(value)
        raise ValueError('Cannot create ULID from string of length {}'.format(len_value))
    if isinstance(value, (int, float)):
        return from_int(int(value))
    if isinstance(value, (bytes, bytearray)):
        return from_bytes(value)
    if isinstance(value, memoryview):
        return from_bytes(value.tobytes())
    raise ValueError('Cannot create ULID from type {}'.format(value.__class__.__name__))


def create(timestamp: codec.TimestampPrimitive, randomness: codec.RandomnessPrimitive) -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance using the given timestamp and randomness values.

    The following types are supported for timestamp values:

    * :class:`~datetime.datetime`
    * :class:`~int`
    * :class:`~float`
    * :class:`~str`
    * :class:`~memoryview`
    * :class:`~ulid.ulid.Timestamp`
    * :class:`~ulid.ulid.ULID`
    * :class:`~bytes`
    * :class:`~bytearray`

    The following types are supported for randomness values:

    * :class:`~int`
    * :class:`~float`
    * :class:`~str`
    * :class:`~memoryview`
    * :class:`~ulid.ulid.Randomness`
    * :class:`~ulid.ulid.ULID`
    * :class:`~bytes`
    * :class:`~bytearray`

    :param timestamp: Unix timestamp in seconds
    :type timestamp: See docstring for types
    :param randomness: Random bytes
    :type randomness: See docstring for types
    :return: ULID using given timestamp and randomness
    :rtype: :class:`~ulid.ulid.ULID`
    :raises ValueError: when a value is an unsupported type
    :raises ValueError: when a value is a string and cannot be Base32 decoded
    :raises ValueError: when a value is or was converted to incorrect bit length
    """
    timestamp = codec.decode_timestamp(timestamp)
    randomness = codec.decode_randomness(randomness)
    return ulid.ULID(timestamp.bytes + randomness.bytes)


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
    if value < 0:
        raise ValueError('Expects positive integer')

    length = (value.bit_length() + 7) // 8
    if length > 16:
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


def from_timestamp(timestamp: codec.TimestampPrimitive) -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance using a timestamp value of a supported type.

    The following types are supported for timestamp values:

    * :class:`~datetime.datetime`
    * :class:`~int`
    * :class:`~float`
    * :class:`~str`
    * :class:`~memoryview`
    * :class:`~ulid.ulid.Timestamp`
    * :class:`~ulid.ulid.ULID`
    * :class:`~bytes`
    * :class:`~bytearray`

    :param timestamp: Unix timestamp in seconds
    :type timestamp: See docstring for types
    :return: ULID using given timestamp and new randomness
    :rtype: :class:`~ulid.ulid.ULID`
    :raises ValueError: when the value is an unsupported type
    :raises ValueError: when the value is a string and cannot be Base32 decoded
    :raises ValueError: when the value is or was converted to something 48 bits
    """
    return create(timestamp, os.urandom(10))


def from_randomness(randomness: codec.RandomnessPrimitive) -> ulid.ULID:
    """
    Create a new :class:`~ulid.ulid.ULID` instance using the given randomness value of a supported type.

    The following types are supported for randomness values:

    * :class:`~int`
    * :class:`~float`
    * :class:`~str`
    * :class:`~memoryview`
    * :class:`~ulid.ulid.Randomness`
    * :class:`~ulid.ulid.ULID`
    * :class:`~bytes`
    * :class:`~bytearray`

    :param randomness: Random bytes
    :type randomness: See docstring for types
    :return: ULID using new timestamp and given randomness
    :rtype: :class:`~ulid.ulid.ULID`
    :raises ValueError: when the value is an unsupported type
    :raises ValueError: when the value is a string and cannot be Base32 decoded
    :raises ValueError: when the value is or was converted to something 80 bits
    """
    return create(int(time.time() * 1000).to_bytes(6, byteorder='big'), randomness)
