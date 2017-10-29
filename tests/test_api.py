"""
    test_api
    ~~~~~~~~

    Tests for the :mod:`~ulid.api` module.
"""
import datetime
import pytest
import time
import uuid

from ulid import api, base32, ulid


BYTES_SIZE_EXC_REGEX = r'Expects bytes to be 128 bits'
INT_SIZE_EXC_REGEX = r'Expects integer to be 128 bits'
STR_SIZE_EXC_REGEX = r'Expects 26 characters'
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


@pytest.fixture('session', params=[bytes, bytearray, memoryview])
def buffer_type(request):
    """
    Fixture that yields types that support the buffer protocol.
    """
    return request.param


def test_new_returns_ulid_instance():
    """
    Assert that :func:`~ulid.api.new` returns a new :class:`~ulid.ulid.ULID` instance.
    """
    assert isinstance(api.new(), ulid.ULID)


def test_from_bytes_returns_ulid_instance(buffer_type, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_bytes` returns a new :class:`~ulid.ulid.ULID` instance
    from the given bytes.
    """
    value = buffer_type(valid_bytes_128)
    instance = api.from_bytes(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == valid_bytes_128


def test_from_bytes_raises_when_not_128_bits(buffer_type, invalid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_bytes` raises a :class:`~ValueError` when given bytes
    that is not 128 bit in length.
    """
    value = buffer_type(invalid_bytes_128)
    with pytest.raises(ValueError) as ex:
        api.from_bytes(value)
    assert ex.match(BYTES_SIZE_EXC_REGEX)


def test_from_int_returns_ulid_instance(valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_int` returns a new :class:`~ulid.ulid.ULID` instance
    from the given bytes.
    """
    value = int.from_bytes(valid_bytes_128, byteorder='big')
    instance = api.from_int(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == valid_bytes_128


def test_from_int_raises_when_not_128_bits(invalid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_int` raises a :class:`~ValueError` when given bytes
    that is not 128 bit in length.
    """
    value = int.from_bytes(invalid_bytes_128, byteorder='big')
    with pytest.raises(ValueError) as ex:
        api.from_int(value)
    assert ex.match(INT_SIZE_EXC_REGEX)


def test_from_str_returns_ulid_instance(valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_str` returns a new :class:`~ulid.ulid.ULID` instance
    from the given bytes.
    """
    value = base32.encode(valid_bytes_128)
    instance = api.from_str(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == valid_bytes_128


def test_from_str_raises_when_not_128_bits(valid_bytes_48):
    """
    Assert that :func:`~ulid.api.from_str` raises a :class:`~ValueError` when given bytes
    that is not 128 bit in length.
    """
    value = base32.encode(valid_bytes_48)
    with pytest.raises(ValueError) as ex:
        api.from_str(value)
    assert ex.match(STR_SIZE_EXC_REGEX)


def test_from_uuid_returns_ulid_instance():
    """
    Assert that :func:`~ulid.api.from_uuid` returns a new :class:`~ulid.ulid.ULID` instance
    from the underlying bytes of the UUID.
    """
    value = uuid.uuid4()
    instance = api.from_uuid(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == value.bytes


def test_from_timestamp_datetime_returns_ulid_instance():
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given Unix time from epoch in seconds as an :class:`~datetime.dateime`.
    """
    value = datetime.datetime.now()
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert int(instance.timestamp().timestamp) == int(value.timestamp())


def test_from_timestamp_int_returns_ulid_instance():
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given Unix time from epoch in seconds as an :class:`~int`.
    """
    value = int(time.time())
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert int(instance.timestamp().timestamp) == value


def test_from_timestamp_float_returns_ulid_instance():
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given Unix time from epoch in seconds as a :class:`~float`.
    """
    value = float(time.time())
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert int(instance.timestamp().timestamp) == int(value)


def test_from_timestamp_str_returns_ulid_instance(valid_bytes_48):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as a :class:`~str`.
    """
    value = base32.encode_timestamp(valid_bytes_48)
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp().str == value


def test_from_timestamp_bytes_returns_ulid_instance(buffer_type, valid_bytes_48):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as an object that supports the buffer protocol.
    """
    value = buffer_type(valid_bytes_48)
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp().bytes == value


def test_from_timestamp_timestamp_returns_ulid_instance(valid_bytes_48):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as a :class:`~ulid.ulid.Timestamp`.
    """
    value = ulid.Timestamp(valid_bytes_48)
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp() == value


def test_from_timestamp_ulid_returns_ulid_instance(valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as a :class:`~ulid.ulid.ULID`.
    """
    value = ulid.ULID(valid_bytes_128)
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp() == value.timestamp()


def test_from_timestamp_with_unsupported_type_raises(unsupported_type):
    """
    Assert that :func:`~ulid.api.from_timestamp` raises a :class:`~ValueError` when given
    a type it cannot compute a timestamp value from.
    """
    with pytest.raises(ValueError) as ex:
        api.from_timestamp(unsupported_type())
    assert ex.match(UNSUPPORTED_TIMESTAMP_TYPE_EXC_REGEX)


def test_from_timestamp_with_incorrect_size_bytes_raises(valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_timestamp` raises a :class:`~ValueError` when given
    a type that cannot be represented as exactly 48 bits.
    """
    with pytest.raises(ValueError) as ex:
        api.from_timestamp(valid_bytes_128)
    assert ex.match(TIMESTAMP_SIZE_EXC_REGEX)


def test_from_randomness_int_returns_ulid_instance(valid_bytes_80):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an :class:`~int`.
    """
    value = int.from_bytes(valid_bytes_80, byteorder='big')
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().int == value


def test_from_randomness_float_returns_ulid_instance(valid_bytes_80):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an :class:`~float`.
    """
    value = float(int.from_bytes(valid_bytes_80, byteorder='big'))
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().int == int(value)


def test_from_randomness_str_returns_ulid_instance(valid_bytes_80):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an :class:`~str`.
    """
    value = base32.encode_randomness(valid_bytes_80)
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().str == value


def test_from_randomness_bytes_returns_ulid_instance(buffer_type, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an object that supports the buffer protocol.
    """
    value = buffer_type(valid_bytes_80)
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().bytes == value


def test_from_randomness_randomness_returns_ulid_instance(valid_bytes_80):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as a :class:`~ulid.ulid.Randomness`.
    """
    value = ulid.Randomness(valid_bytes_80)
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness() == value


def test_from_randomness_ulid_returns_ulid_instance(valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as a :class:`~ulid.ulid.ULID`.
    """
    value = ulid.ULID(valid_bytes_128)
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness() == value.randomness()


def test_from_randomness_with_unsupported_type_raises(unsupported_type):
    """
    Assert that :func:`~ulid.api.from_randomness` raises a :class:`~ValueError` when given
    a type it cannot compute a randomness value from.
    """
    with pytest.raises(ValueError) as ex:
        api.from_randomness(unsupported_type())
    assert ex.match(UNSUPPORTED_RANDOMNESS_TYPE_EXC_REGEX)


def test_from_randomness_with_incorrect_size_bytes_raises(valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_randomness` raises a :class:`~ValueError` when given
    a type that cannot be represented as exactly 80 bits.
    """
    with pytest.raises(ValueError) as ex:
        api.from_randomness(valid_bytes_128)
    assert ex.match(RANDOMNESS_SIZE_EXC_REGEX)
