"""
    test_codec
    ~~~~~~~~~~

    Tests for the :mod:`~ulid.codec` module.
"""
import datetime
import time

import pytest

from ulid import base32, codec, ulid

UNSUPPORTED_TIMESTAMP_TYPE_EXC_REGEX = (r'Expected datetime, int, float, str, memoryview, Timestamp'
                                        r', ULID, bytes, or bytearray')
TIMESTAMP_SIZE_EXC_REGEX = r'Expects timestamp to be 48 bits'
UNSUPPORTED_RANDOMNESS_TYPE_EXC_REGEX = r'Expected int, float, str, memoryview, Randomness, ULID, bytes, or bytearray'
RANDOMNESS_SIZE_EXC_REGEX = r'Expects randomness to be 80 bits'


@pytest.fixture(scope='session', params=[
    list,
    dict,
    set,
    tuple,
    type(None)
])
def unsupported_type(request):
    """
    Fixture that yields types that a cannot be converted to a timestamp/randomness.
    """
    return request.param


@pytest.fixture(scope='session', params=[bytes, bytearray, memoryview])
def buffer_type(request):
    """
    Fixture that yields types that support the buffer protocol.
    """
    return request.param


def test_decode_timestamp_datetime_returns_timestamp_instance():
    """
    Assert that :func:`~ulid.codec.decode_timestamp` returns a new :class:`~ulid.ulid.Timestamp` instance
    from the given Unix time from epoch in seconds as an :class:`~datetime.datetime`.
    """
    value = datetime.datetime.now()
    instance = codec.decode_timestamp(value)
    assert isinstance(instance, ulid.Timestamp)
    assert int(instance.timestamp) == int(value.timestamp())


def test_decode_timestamp_int_returns_timestamp_instance():
    """
    Assert that :func:`~ulid.codec.decode_timestamp` returns a new :class:`~ulid.ulid.Timestamp` instance
    from the given Unix time from epoch in seconds as an :class:`~int`.
    """
    value = int(time.time())
    instance = codec.decode_timestamp(value)
    assert isinstance(instance, ulid.Timestamp)
    assert int(instance.timestamp) == value


def test_decode_timestamp_float_returns_timestamp_instance():
    """
    Assert that :func:`~ulid.codec.decode_timestamp` returns a new :class:`~ulid.ulid.Timestamp` instance
    from the given Unix time from epoch in seconds as a :class:`~float`.
    """
    value = float(time.time())
    instance = codec.decode_timestamp(value)
    assert isinstance(instance, ulid.Timestamp)
    assert int(instance.timestamp) == int(value)


def test_decode_timestamp_str_returns_timestamp_instance(valid_bytes_48):
    """
    Assert that :func:`~ulid.codec.decode_timestamp` returns a new :class:`~ulid.ulid.Timestamp` instance
    from the given timestamp as a :class:`~str`.
    """
    value = base32.encode_timestamp(valid_bytes_48)
    instance = codec.decode_timestamp(value)
    assert isinstance(instance, ulid.Timestamp)
    assert instance.str == value


def test_decode_timestamp_bytes_returns_timestamp_instance(buffer_type, valid_bytes_48):
    """
    Assert that :func:`~ulid.codec.decode_timestamp` returns a new :class:`~ulid.ulid.Timestamp` instance
    from the given timestamp as an object that supports the buffer protocol.
    """
    value = buffer_type(valid_bytes_48)
    instance = codec.decode_timestamp(value)
    assert isinstance(instance, ulid.Timestamp)
    assert instance.bytes == value


def test_decode_timestamp_timestamp_returns_timestamp_instance(valid_bytes_48):
    """
    Assert that :func:`~ulid.codec.decode_timestamp` returns a new :class:`~ulid.ulid.Timestamp` instance
    from the given timestamp as a :class:`~ulid.ulid.Timestamp`.
    """
    value = ulid.Timestamp(valid_bytes_48)
    instance = codec.decode_timestamp(value)
    assert isinstance(instance, ulid.Timestamp)
    assert instance == value


def test_decode_timestamp_ulid_returns_timestamp_instance(valid_bytes_128):
    """
    Assert that :func:`~ulid.codec.decode_timestamp` returns a new :class:`~ulid.ulid.Timestamp` instance
    from the given timestamp as a :class:`~ulid.ulid.ULID`.
    """
    value = ulid.ULID(valid_bytes_128)
    instance = codec.decode_timestamp(value)
    assert isinstance(instance, ulid.Timestamp)
    assert instance == value.timestamp()


def test_decode_timestamp_with_unsupported_type_raises(unsupported_type):
    """
    Assert that :func:`~ulid.codec.decode_timestamp` raises a :class:`~ValueError` when given
    a type it cannot compute a timestamp value from.
    """
    with pytest.raises(ValueError) as ex:
       codec.decode_timestamp(unsupported_type())
    assert ex.match(UNSUPPORTED_TIMESTAMP_TYPE_EXC_REGEX)


def test_decode_timestamp_with_incorrect_size_bytes_raises(valid_bytes_128):
    """
    Assert that :func:`~ulid.codec.decode_timestamp` raises a :class:`~ValueError` when given
    a type that cannot be represented as exactly 48 bits.
    """
    with pytest.raises(ValueError) as ex:
       codec.decode_timestamp(valid_bytes_128)
    assert ex.match(TIMESTAMP_SIZE_EXC_REGEX)


def test_decode_randomness_int_returns_randomness_instance(valid_bytes_80):
    """
    Assert that :func:`~ulid.codec.decode_randomness` returns a new :class:`~ulid.ulid.Randomness` instance
    from the given random values as an :class:`~int`.
    """
    value = int.from_bytes(valid_bytes_80, byteorder='big')
    instance = codec.decode_randomness(value)
    assert isinstance(instance, ulid.Randomness)
    assert instance.int == value


def test_decode_randomness_float_returns_randomness_instance(valid_bytes_80):
    """
    Assert that :func:`~ulid.codec.decode_randomness` returns a new :class:`~ulid.ulid.Randomness` instance
    from the given random values as an :class:`~float`.
    """
    value = float(int.from_bytes(valid_bytes_80, byteorder='big'))
    instance = codec.decode_randomness(value)
    assert isinstance(instance, ulid.Randomness)
    assert instance.int == int(value)


def test_decode_randomness_str_returns_randomness_instance(valid_bytes_80):

    """
    Assert that :func:`~ulid.codec.decode_randomness` returns a new :class:`~ulid.ulid.Randomness` instance
    from the given random values as an :class:`~str`.
    """
    value = base32.encode_randomness(valid_bytes_80)
    instance = codec.decode_randomness(value)
    assert isinstance(instance, ulid.Randomness)
    assert instance.str == value


def test_decode_randomness_bytes_returns_randomness_instance(buffer_type, valid_bytes_80):
    """
    Assert that :func:`~ulid.codec.decode_randomness` returns a new :class:`~ulid.ulid.Randomness` instance
    from the given random values as an object that supports the buffer protocol.
    """
    value = buffer_type(valid_bytes_80)
    instance = codec.decode_randomness(value)
    assert isinstance(instance, ulid.Randomness)
    assert instance.bytes == value


def test_decode_randomness_randomness_returns_randomness_instance(valid_bytes_80):
    """
    Assert that :func:`~ulid.codec.decode_randomness` returns a new :class:`~ulid.ulid.Randomness` instance
    from the given random values as a :class:`~ulid.ulid.Randomness`.
    """
    value = ulid.Randomness(valid_bytes_80)
    instance = codec.decode_randomness(value)
    assert isinstance(instance, ulid.Randomness)
    assert instance == value


def test_decode_randomness_ulid_returns_randomness_instance(valid_bytes_128):
    """
    Assert that :func:`~ulid.codec.decode_randomness` returns a new :class:`~ulid.ulid.Randomness` instance
    from the given random values as a :class:`~ulid.ulid.ULID`.
    """
    value = ulid.ULID(valid_bytes_128)
    instance = codec.decode_randomness(value)
    assert isinstance(instance, ulid.Randomness)
    assert instance == value.randomness()


def test_decode_randomness_with_unsupported_type_raises(unsupported_type):
    """
    Assert that :func:`~ulid.codec.decode_randomness` raises a :class:`~ValueError` when given
    a type it cannot compute a randomness value from.
    """
    with pytest.raises(ValueError) as ex:
        codec.decode_randomness(unsupported_type())
    assert ex.match(UNSUPPORTED_RANDOMNESS_TYPE_EXC_REGEX)


def test_decode_randomness_with_incorrect_size_bytes_raises(valid_bytes_128):
    """
    Assert that :func:`~ulid.codec.decode_randomness` raises a :class:`~ValueError` when given
    a type that cannot be represented as exactly 80 bits.
    """
    with pytest.raises(ValueError) as ex:
        codec.decode_randomness(valid_bytes_128)
    assert ex.match(RANDOMNESS_SIZE_EXC_REGEX)
