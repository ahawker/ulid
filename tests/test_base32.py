"""
    test_base32
    ~~~~~~~~~~~

    Tests for the :mod:`~ulid.base32` module.
"""
import pytest

from ulid import base32


def test_encode_handles_ulid_and_returns_26_char_string(valid_bytes_128):
    """
    Assert that :func:`~ulid.base32.encode` encodes a valid 128 bit bytes object into a :class:`~str`
    that is 26 characters long.
    """
    encoded = base32.encode(valid_bytes_128)
    assert isinstance(encoded, str)
    assert len(encoded) == 26


def test_encode_handles_timestamp_and_returns_10_char_string(valid_bytes_48):
    """
    Assert that :func:`~ulid.base32.encode` encodes a valid 48 bit bytes object into a :class:`~str`
    that is 10 characters long.
    """
    encoded = base32.encode(valid_bytes_48)
    assert isinstance(encoded, str)
    assert len(encoded) == 10


def test_encode_handles_randomness_and_returns_16_char_string(valid_bytes_80):
    """
    Assert that :func:`~ulid.base32.encode` encodes a valid 80 bit bytes object into a :class:`~str`
    that is 16 characters long.
    """
    encoded = base32.encode(valid_bytes_80)
    assert isinstance(encoded, str)
    assert len(encoded) == 16


def test_encode_raises_on_bytes_length_mismatch(invalid_bytes_48_80_128):
    """
    Assert that :func:`~ulid.base32.encode` raises a :class:`~ValueError` when given a :class:`~bytes`
    instance that is not exactly 48, 80, or 128 bits in length.
    """
    with pytest.raises(ValueError):
        base32.encode(invalid_bytes_48_80_128)


def test_encode_ulid_returns_26_char_string(valid_bytes_128):
    """
    Assert that :func:`~ulid.base32.encode_ulid` encodes a valid 128 bit bytes object into a :class:`~str`
    that is 26 characters long.
    """
    encoded = base32.encode_ulid(valid_bytes_128)
    assert isinstance(encoded, str)
    assert len(encoded) == 26


def test_encode_ulid_raises_on_bytes_length_mismatch(invalid_bytes_128):
    """
    Assert that :func:`~ulid.base32.encode_ulid` raises a :class:`~ValueError` when given a :class:`~bytes`
    instance that is not exactly 128 bit.
    """
    with pytest.raises(ValueError):
        base32.encode_ulid(invalid_bytes_128)


def test_encode_timestamp_returns_10_char_string(valid_bytes_48):
    """
    Assert that :func:`~ulid.base32.encode_timestamp` encodes a valid 48 bit bytes object into a :class:`~str`
    that is 10 characters long.
    """
    encoded = base32.encode_timestamp(valid_bytes_48)
    assert isinstance(encoded, str)
    assert len(encoded) == 10


def test_encode_timestamp_raises_on_bytes_length_mismatch(invalid_bytes_48):
    """
    Assert that :func:`~ulid.base32.encode_timestamp` raises a :class:`~ValueError` when given a :class:`~bytes`
    instance that is not exactly 48 bit.
    """
    with pytest.raises(ValueError):
        base32.encode_timestamp(invalid_bytes_48)


def test_encode_randomness_returns_16_char_string(valid_bytes_80):
    """
    Assert that :func:`~ulid.base32.encode_randomness` encodes a valid 80 bit bytes object into a :class:`~str`
    that is 16 characters long.
    """
    encoded = base32.encode_randomness(valid_bytes_80)
    assert isinstance(encoded, str)
    assert len(encoded) == 16


def test_encode_randomness_raises_on_bytes_length_mismatch(invalid_bytes_80):
    """
    Assert that :func:`~ulid.base32.encode_randomness` raises a :class:`~ValueError` when given a :class:`~bytes`
    instance that is not exactly 80 bit.
    """
    with pytest.raises(ValueError):
        base32.encode_randomness(invalid_bytes_80)
