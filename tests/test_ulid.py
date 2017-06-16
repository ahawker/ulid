"""
    test_ulid
    ~~~~~~~~~

    Tests for the :mod:`~ulid.ulid` module.
"""
import datetime
import pytest
import time
import uuid

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


def test_memoryview_supports_eq_with_expected_types(valid_bytes_128):
    """
    Assert that :class:`~ulid.ulid.MemoryView` supports "equal" comparisons against expected types.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert mv == ulid.MemoryView(valid_bytes_128)
    assert mv == bytes(valid_bytes_128)
    assert mv == bytearray(valid_bytes_128)
    assert mv == memoryview(valid_bytes_128)
    assert mv == int.from_bytes(valid_bytes_128, byteorder='big')
    assert mv == base32.encode(valid_bytes_128)


def test_memoryview_supports_ne_with_expected_types(valid_bytes_128, valid_bytes_80):
    """
    Assert that :class:`~ulid.ulid.MemoryView` supports "not equal" comparisons against expected types.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert mv != ulid.MemoryView(valid_bytes_80)
    assert mv != bytes(valid_bytes_80)
    assert mv != bytearray(valid_bytes_80)
    assert mv != memoryview(valid_bytes_80)
    assert mv != int.from_bytes(valid_bytes_80, byteorder='big')
    assert mv != base32.encode(valid_bytes_80)


def test_memoryview_supports_lt_with_expected_types(ulid_bytes_year_1990, ulid_bytes_year_2000):
    """
    Assert that :class:`~ulid.ulid.MemoryView` supports "less than" comparisons against expected types.
    """
    mv = ulid.MemoryView(ulid_bytes_year_1990)
    assert mv < ulid.MemoryView(ulid_bytes_year_2000)
    assert mv < bytes(ulid_bytes_year_2000)
    assert mv < bytearray(ulid_bytes_year_2000)
    assert mv < memoryview(ulid_bytes_year_2000)
    assert mv < int.from_bytes(ulid_bytes_year_2000, byteorder='big')
    assert mv < base32.encode(ulid_bytes_year_2000)


def test_memoryview_supports_gt_with_expected_types(ulid_bytes_year_1990, ulid_bytes_year_2000):
    """
    Assert that :class:`~ulid.ulid.MemoryView` supports "greater than" comparisons against expected types.
    """
    mv = ulid.MemoryView(ulid_bytes_year_2000)
    assert mv > ulid.MemoryView(ulid_bytes_year_1990)
    assert mv > bytes(ulid_bytes_year_1990)
    assert mv > bytearray(ulid_bytes_year_1990)
    assert mv > memoryview(ulid_bytes_year_1990)
    assert mv > int.from_bytes(ulid_bytes_year_1990, byteorder='big')
    assert mv > base32.encode(ulid_bytes_year_1990)


def test_memoryview_supports_le_with_expected_types(ulid_bytes_year_1990, ulid_bytes_year_2000):
    """
    Assert that :class:`~ulid.ulid.MemoryView` supports "less than or equals" comparisons against expected types.
    """
    mv = ulid.MemoryView(ulid_bytes_year_1990)
    assert mv <= ulid.MemoryView(ulid_bytes_year_1990)
    assert mv <= ulid.MemoryView(ulid_bytes_year_2000)
    assert mv <= bytes(ulid_bytes_year_2000)
    assert mv <= bytearray(ulid_bytes_year_2000)
    assert mv <= memoryview(ulid_bytes_year_2000)
    assert mv <= int.from_bytes(ulid_bytes_year_2000, byteorder='big')
    assert mv <= base32.encode(ulid_bytes_year_2000)


def test_memoryview_supports_ge_with_expected_types(ulid_bytes_year_1990, ulid_bytes_year_2000):
    """
    Assert that :class:`~ulid.ulid.MemoryView` supports "greater than or equals" comparisons against expected types.
    """
    mv = ulid.MemoryView(ulid_bytes_year_2000)
    assert mv >= ulid.MemoryView(ulid_bytes_year_1990)
    assert mv >= ulid.MemoryView(ulid_bytes_year_1990)
    assert mv >= bytes(ulid_bytes_year_1990)
    assert mv >= bytearray(ulid_bytes_year_1990)
    assert mv >= memoryview(ulid_bytes_year_1990)
    assert mv >= int.from_bytes(ulid_bytes_year_1990, byteorder='big')
    assert mv >= base32.encode(ulid_bytes_year_1990)


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
    with pytest.raises(TypeError):
        mv < unsupported_comparison_type()
    with pytest.raises(TypeError):
        mv > unsupported_comparison_type()
    with pytest.raises(TypeError):
        mv <= unsupported_comparison_type()
    with pytest.raises(TypeError):
        mv >= unsupported_comparison_type()


def test_memoryview_supports_str(valid_bytes_128):
    """
    Assert that the `str` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    result of the :meth:`~ulid.ulid.MemoryView.str` method.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert str(mv) == mv.str()


def test_memoryview_supports_int(valid_bytes_128):
    """
    Assert that the `int` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    result of the :meth:`~ulid.ulid.MemoryView.int` method.
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert int(mv) == mv.int()


def test_memoryview_defines_hash(valid_bytes_128):
    """
    Assert that the `hash` representation of a :class:`~ulid.ulid.MemoryView` is equal to the
    hash result of the underlying :class:`~memoryview.`
    """
    mv = ulid.MemoryView(valid_bytes_128)
    assert hash(mv) == hash(mv.memory)


def test_timestamp_coverts_bytes_to_unix_time_seconds():
    """
    Assert that :meth:`~ulid.ulid.Timestamp.timestamp` returns the value in Unix time in seconds from epoch.
    """
    now_ms = int(time.time()) * 1000
    timestamp = ulid.Timestamp(now_ms.to_bytes(6, byteorder='big'))
    assert timestamp.timestamp() == now_ms / 1000.0


def test_timestamp_converts_to_datetime():
    """
    Assert that :meth:`~ulid.ulid.Timestamp.datetime` returns the value as
    a :class:`~datetime.dateime` instance.
    """
    now_ms = int(time.time()) * 1000
    timestamp = ulid.Timestamp(now_ms.to_bytes(6, byteorder='big'))
    assert timestamp.datetime() == datetime.datetime.utcfromtimestamp(now_ms / 1000.0)


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
    assert timestamp.bytes() == valid_bytes_128[:6]


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
    assert randomness.bytes() == valid_bytes_128[6:]


def test_ulid_uuid_returns_instance(valid_bytes_128):
    """
    Assert that :func:`~ulid.ulid.ULID.uuid` returns a :class:`~uuid.UUID` instance.
    """
    assert isinstance(ulid.ULID(valid_bytes_128).uuid(), uuid.UUID)
