"""
    test_ulid
    ~~~~~~~~~

    Tests for the :mod:`~ulid.ulid` module.
"""
import copy
import datetime
import operator
import pickle
import time
import uuid

import pytest

from ulid import base32, ulid


@pytest.fixture(scope='session', params=[
    list,
    dict,
    set,
    tuple,
    type(None)
])
def unsupported_comparison_type(request):
    """
    Fixture that yields types that a :class:`~ulid.ulid.MemoryView` cannot be compared with.
    """
    return request.param


@pytest.fixture(scope='session', params=[
    ulid.MemoryView,
    ulid.Timestamp,
    ulid.Randomness,
    ulid.ULID
])
def model_types(request):
    """
    Fixture that yields a model type that is assignable from :class:`~ulid.ulid.MemoryView`.
    """
    return request.param


@pytest.fixture(scope='function')
def model_with_eq_bytes(model_types, valid_bytes_128, valid_bytes_80, valid_bytes_48):
    """
    Fixture that yields a model type along with a valid collection of bytes for an equality check.
    """
    if model_types in (ulid.MemoryView, ulid.ULID):
        return model_types, valid_bytes_128
    if model_types == ulid.Randomness:
        return model_types, valid_bytes_80
    if model_types == ulid.Timestamp:
        return model_types, valid_bytes_48


@pytest.fixture(scope='function')
def model_with_ne_bytes(model_types, valid_bytes_128, valid_bytes_80, valid_bytes_48):
    """
    Fixture that yields a model type, a valid collection of bytes of an equality check, and
    a valid collection of bytes for an inequality check.
    """
    if model_types in (ulid.MemoryView, ulid.ULID):
        return model_types, valid_bytes_128, valid_bytes_80
    if model_types == ulid.Randomness:
        return model_types, valid_bytes_80, valid_bytes_128
    if model_types == ulid.Timestamp:
        return model_types, valid_bytes_48, valid_bytes_128


@pytest.fixture(scope='function')
def model_with_ordered_bytes(model_types, valid_bytes_128_before, valid_bytes_128_after,
                             valid_bytes_80_before, valid_bytes_80_after,
                             valid_bytes_48_before, valid_bytes_48_after):
    """
    Fixture that yields a model type, a valid collection of before that are "less than", and
    a valid collection of bytes that are "greater than" the "less than" collection of bytes.
    """
    if model_types in (ulid.MemoryView, ulid.ULID):
        return model_types, valid_bytes_128_before, valid_bytes_128_after
    if model_types == ulid.Randomness:
        return model_types, valid_bytes_80_before, valid_bytes_80_after
    if model_types == ulid.Timestamp:
        return model_types, valid_bytes_48_before, valid_bytes_48_after


def test_model_supports_eq_with_expected_types(model_with_eq_bytes):
    """
    Assert that any of the model types support "equal" comparisons against expected types.
    """
    model_type, equal_bytes = model_with_eq_bytes

    model = model_type(equal_bytes)
    assert model == model_type(equal_bytes)
    assert model == bytes(equal_bytes)
    assert model == bytearray(equal_bytes)
    assert model == memoryview(equal_bytes)
    assert model == int.from_bytes(equal_bytes, byteorder='big')
    assert model == float(int.from_bytes(equal_bytes, byteorder='big'))
    assert model == base32.encode(equal_bytes)


def test_model_supports_ne_with_expected_types(model_with_ne_bytes):
    """
    Assert that any of the model types supports "not equal" comparisons against expected types.
    """
    model_type, equal_bytes, not_equal_bytes = model_with_ne_bytes

    model = model_type(equal_bytes)
    assert model != ulid.MemoryView(not_equal_bytes)
    assert model != bytes(not_equal_bytes)
    assert model != bytearray(not_equal_bytes)
    assert model != memoryview(not_equal_bytes)
    assert model != int.from_bytes(not_equal_bytes, byteorder='big')
    assert model != float(int.from_bytes(not_equal_bytes, byteorder='big'))
    assert model != base32.encode(not_equal_bytes)


def test_model_supports_lt_with_expected_types(model_with_ordered_bytes):
    """
    Assert that any of the model types support "less than" comparisons against expected types.
    """
    model_type, less_than_bytes, greater_than_bytes = model_with_ordered_bytes

    model = model_type(less_than_bytes)
    assert model < ulid.MemoryView(greater_than_bytes)
    assert model < bytes(greater_than_bytes)
    assert model < bytearray(greater_than_bytes)
    assert model < memoryview(greater_than_bytes)
    assert model < int.from_bytes(greater_than_bytes, byteorder='big')
    assert model < float(int.from_bytes(greater_than_bytes, byteorder='big'))
    assert model < base32.encode(greater_than_bytes)


def test_model_supports_gt_with_expected_types(model_with_ordered_bytes):
    """
    Assert that any of the model types support "greater than" comparisons against expected types.
    """
    model_type, less_than_bytes, greater_than_bytes = model_with_ordered_bytes

    model = model_type(greater_than_bytes)
    assert model > ulid.MemoryView(less_than_bytes)
    assert model > bytes(less_than_bytes)
    assert model > bytearray(less_than_bytes)
    assert model > memoryview(less_than_bytes)
    assert model > int.from_bytes(less_than_bytes, byteorder='big')
    assert model > float(int.from_bytes(less_than_bytes, byteorder='big'))
    assert model > base32.encode(less_than_bytes)


def test_model_supports_le_with_expected_types(model_with_ordered_bytes):
    """
    Assert that any of the model types support "less than or equal" comparisons against expected types.
    """
    model_type, less_than_bytes, greater_than_bytes = model_with_ordered_bytes

    model = model_type(less_than_bytes)
    assert model <= ulid.MemoryView(less_than_bytes)
    assert model <= bytes(less_than_bytes)
    assert model <= bytearray(less_than_bytes)
    assert model <= memoryview(less_than_bytes)
    assert model <= int.from_bytes(less_than_bytes, byteorder='big')
    assert model <= float(int.from_bytes(less_than_bytes, byteorder='big'))
    assert model <= base32.encode(less_than_bytes)

    assert model <= ulid.MemoryView(greater_than_bytes)
    assert model <= bytes(greater_than_bytes)
    assert model <= bytearray(greater_than_bytes)
    assert model <= memoryview(greater_than_bytes)
    assert model <= int.from_bytes(greater_than_bytes, byteorder='big')
    assert model <= float(int.from_bytes(greater_than_bytes, byteorder='big'))
    assert model <= base32.encode(greater_than_bytes)


def test_model_supports_ge_with_expected_types(model_with_ordered_bytes):
    """
    Assert that any of the model types support "greater than or equal" comparisons against expected types.
    """
    model_type, less_than_bytes, greater_than_bytes = model_with_ordered_bytes

    model = model_type(greater_than_bytes)
    assert model >= ulid.MemoryView(greater_than_bytes)
    assert model >= bytes(greater_than_bytes)
    assert model >= bytearray(greater_than_bytes)
    assert model >= memoryview(greater_than_bytes)
    assert model >= int.from_bytes(greater_than_bytes, byteorder='big')
    assert model >= float(int.from_bytes(greater_than_bytes, byteorder='big'))
    assert model >= base32.encode(greater_than_bytes)

    assert model >= ulid.MemoryView(less_than_bytes)
    assert model >= bytes(less_than_bytes)
    assert model >= bytearray(less_than_bytes)
    assert model >= memoryview(less_than_bytes)
    assert model >= int.from_bytes(less_than_bytes, byteorder='big')
    assert model >= float(int.from_bytes(less_than_bytes, byteorder='big'))
    assert model >= base32.encode(less_than_bytes)


def test_memoryview_eq_false_with_unsupported_type(valid_bytes_128, unsupported_comparison_type):
    """
    Assert that :class:`~ulid.ulid.MemoryView` returns `False` on "equal" comparisons
    against unsupported types.
    """
    assert not ulid.MemoryView(valid_bytes_128) == unsupported_comparison_type()


def test_memoryview_ne_false_with_unsupported_type(valid_bytes_128, unsupported_comparison_type):
    """
    Assert that :class:`~ulid.ulid.MemoryView` returns `True` on "not equal" comparisons
    against unsupported types.
    """
    assert ulid.MemoryView(valid_bytes_128) != unsupported_comparison_type()


def test_memoryview_unorderble_with_unsupported_type(valid_bytes_128, unsupported_comparison_type):
    """
    Assert that :class:`~ulid.ulid.MemoryView` returns `False` on "less than" comparisons
    against unsupported types.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    for op in (operator.lt, operator.gt, operator.le, operator.ge):
        with pytest.raises(TypeError):
            op(mv, unsupported_comparison_type())


def test_memoryview_supports_bin(valid_bytes_128):
    """
    Assert that the `bin` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    result of the :meth:`~ulid.ulid.MemoryView.bin` method.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert bin(mv) == mv.bin


def test_memoryview_supports_hex(valid_bytes_128):
    """
    Assert that the `hex` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    result of the :meth:`~ulid.ulid.MemoryView.hex` method.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert hex(mv) == mv.hex


def test_memoryview_supports_oct(valid_bytes_128):
    """
    Assert that the `oct` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    result of the :meth:`~ulid.ulid.MemoryView.oct` method.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert oct(mv) == mv.oct


def test_memoryview_supports_bytes(valid_bytes_128):
    """
    Assert that the `bytes` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    result of the :meth:`~ulid.ulid.MemoryView.bytes` method.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert bytes(mv) == mv.bytes


def test_memoryview_supports_str(valid_bytes_128):
    """
    Assert that the `str` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    result of the :meth:`~ulid.ulid.MemoryView.str` method.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert str(mv) == mv.str


def test_memoryview_supports_int(valid_bytes_128):
    """
    Assert that the `int` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    result of the :meth:`~ulid.ulid.MemoryView.int` method.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert int(mv) == mv.int


def test_memoryview_supports_float(valid_bytes_128):
    """
    Assert that the `float` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    result of the :meth:`~ulid.ulid.MemoryView.float` method.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert float(mv) == mv.float


def test_memoryview_supports_hash(valid_bytes_128):
    """
    Assert that the `hash` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    hash result of the underlying :class:`~memoryview.`
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert hash(mv) == hash(mv.memory)


def test_memoryview_supports_index(valid_bytes_128):
    """
    Assert that the `__index__` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    int value of the underlying :class:`~memoryview.`
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert mv.__index__() == mv.int


def test_memoryview_supports_getstate(valid_bytes_128):
    """
    Assert that the `__getstate__` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    str result of the underlying :class:`~memoryview.`
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert mv.__getstate__() == mv.str


def test_memoryview_supports_pickle(valid_bytes_128):
    """
    Assert that instances of :class:`~ulid.ulid.MemoryView` can be pickled and use the
    the str result of the underlying :class:`~memoryview.` as the serialized value.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    serialized = pickle.dumps(mv)
    assert serialized is not None
    assert isinstance(serialized, bytes)
    deserialized = pickle.loads(serialized)
    assert deserialized == mv.str


def test_memoryview_supports_copy(valid_bytes_128):
    """
    Assert that instances of :class:`~ulid.ulid.MemoryView` can be copied using
    :func:`~copy.copy`.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    copied = copy.copy(mv)
    assert copied == mv


def test_memoryview_supports_deepcopy(valid_bytes_128):
    """
    Assert that instances of :class:`~ulid.ulid.MemoryView` can be copied using
    :func:`~copy.deepcopy`.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    data = dict(a=dict(b=dict(c=mv)))
    copied = copy.deepcopy(data)
    assert copied == data


def test_timestamp_coverts_bytes_to_unix_time_seconds():
    """
    Assert that :meth:`~ulid.ulid.Timestamp.timestamp` returns the value in Unix time in seconds from epoch.
    """
    now_ms = int(time.time()) * 1000
    timestamp = ulid.Timestamp(now_ms.to_bytes(6, byteorder='big'))
    assert timestamp.timestamp == now_ms / 1000.0


def test_timestamp_converts_to_utc_aware_datetime():
    """
    Assert that :meth:`~ulid.ulid.Timestamp.datetime` returns the value as
    a :class:`~datetime.datetime` instance that is UTC aware.
    """
    now_ms = int(time.time()) * 1000
    timezone = datetime.timezone.utc
    timestamp = ulid.Timestamp(now_ms.to_bytes(6, byteorder='big'))
    assert timestamp.datetime == datetime.datetime.utcfromtimestamp(now_ms / 1000.0).replace(tzinfo=timezone)


def test_ulid_timestamp_returns_instance(valid_bytes_128):
    """
    Assert that :meth:`~ulid.ulid.timestamp` returns a :class:`~ulid.ulid.Timestamp` instance.
    """
    assert isinstance(ulid.ULID(valid_bytes_128).timestamp(), ulid.Timestamp)


def test_ulid_timestamp_is_first_48_bits(valid_bytes_128):
    """
    Assert that :meth:`~ulid.ulid.timestamp` returns a :class:`~ulid.ulid.Timestamp` instance that
    is populated with the first 48 bits of the ULID.
    """
    timestamp = ulid.ULID(valid_bytes_128).timestamp()
    assert timestamp.bytes == valid_bytes_128[:6]


def test_ulid_randomness_returns_instance(valid_bytes_128):
    """
    Assert that :meth:`~ulid.ulid.randomness` returns a :class:`~ulid.ulid.Randomness` instance.
    """
    assert isinstance(ulid.ULID(valid_bytes_128).randomness(), ulid.Randomness)


def test_ulid_randomness_is_first_48_bits(valid_bytes_128):
    """
    Assert that :meth:`~ulid.ulid.randomness` returns a :class:`~ulid.ulid.Randomness` instance that
    is populated with the last 80 bits of the ULID.
    """
    randomness = ulid.ULID(valid_bytes_128).randomness()
    assert randomness.bytes == valid_bytes_128[6:]


def test_ulid_uuid_returns_instance(valid_bytes_128):
    """
    Assert that :func:`~ulid.ulid.ULID.uuid` returns a :class:`~uuid.UUID` instance.
    """
    assert isinstance(ulid.ULID(valid_bytes_128).uuid, uuid.UUID)


def test_hex_length_padding(valid_bytes_128):
    """
    Assert that the `hex` representation of a :class:`~ulid.ulid.MemoryView` is
    correctly padded to 32 hex characters (34 with leading '0x').
    """
    mv = ulid.ULID(valid_bytes_128)
    null_ulid = ulid.ULID(b'\00' * 16)
    assert len(mv.hex) == 34
    assert len(null_ulid.hex) == 34
