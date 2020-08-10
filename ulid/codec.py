"""
    ulid/codec
    ~~~~~~~~~~

    Defines encoding/decoding functions for ULID data representations.
"""
import datetime
import typing

from . import base32, hints, ulid

#: Type hint that defines multiple primitive types that can represent
#: a Unix timestamp in seconds.
TimestampPrimitive = typing.Union[hints.Primitive,  # pylint: disable=invalid-name
                                  datetime.datetime, ulid.Timestamp, ulid.ULID]


#: Type hint that defines multiple primitive types that can represent randomness.
RandomnessPrimitive = typing.Union[hints.Primitive, ulid.Randomness, ulid.ULID]  # pylint: disable=invalid-name


def decode_timestamp(timestamp: TimestampPrimitive) -> ulid.Timestamp:
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
    if isinstance(timestamp, datetime.datetime):
        timestamp = timestamp.timestamp()
    if isinstance(timestamp, (int, float)):
        timestamp = int(timestamp * 1000.0).to_bytes(6, byteorder='big')
    elif isinstance(timestamp, str):
        timestamp = base32.decode_timestamp(timestamp)
    elif isinstance(timestamp, memoryview):
        timestamp = timestamp.tobytes()
    elif isinstance(timestamp, ulid.Timestamp):
        timestamp = timestamp.bytes
    elif isinstance(timestamp, ulid.ULID):
        timestamp = timestamp.timestamp().bytes

    if not isinstance(timestamp, (bytes, bytearray)):
        raise ValueError('Expected datetime, int, float, str, memoryview, Timestamp, ULID, '
                         'bytes, or bytearray; got {}'.format(type(timestamp).__name__))

    length = len(timestamp)
    if length != 6:
        raise ValueError('Expects timestamp to be 48 bits; got {} bytes'.format(length))

    return ulid.Timestamp(timestamp)


def decode_randomness(randomness: RandomnessPrimitive) -> ulid.Randomness:
    """
    Create a new :class:`~ulid.ulid.Randomness` instance using the given randomness value of a supported type.

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
    if isinstance(randomness, (int, float)):
        randomness = int(randomness).to_bytes(10, byteorder='big')
    elif isinstance(randomness, str):
        randomness = base32.decode_randomness(randomness)
    elif isinstance(randomness, memoryview):
        randomness = randomness.tobytes()
    elif isinstance(randomness, ulid.Randomness):
        randomness = randomness.bytes
    elif isinstance(randomness, ulid.ULID):
        randomness = randomness.randomness().bytes

    if not isinstance(randomness, (bytes, bytearray)):
        raise ValueError('Expected int, float, str, memoryview, Randomness, ULID, '
                         'bytes, or bytearray; got {}'.format(type(randomness).__name__))

    length = len(randomness)
    if length != 10:
        raise ValueError('Expects randomness to be 80 bits; got {} bytes'.format(length))

    return ulid.Randomness(randomness)
