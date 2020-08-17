"""
    test_module
    ~~~~~~~~~~~

    Tests for the :mod:`~ulid` module.
"""
import pytest

from ulid import consts


def test_min_timestamp_uses_expected_value():
    """
    Assert that :func:`~ulid.consts.MIN_TIMESTAMP` uses expected byte value.
    """
    value = consts.MIN_TIMESTAMP
    assert value == b'\x00\x00\x00\x00\x00\x00'


def test_max_timestamp_uses_expected_value():
    """
    Assert that :func:`~ulid.consts.MAX_RANDOMNESS` uses expected byte value.
    """
    value = consts.MAX_TIMESTAMP
    assert value == b'\xff\xff\xff\xff\xff\xff'


def test_min_randomness_uses_expected_value():
    """
    Assert that :func:`~ulid.consts.MIN_RANDOMNESS` uses expected byte value.
    """
    value = consts.MIN_RANDOMNESS
    assert value == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


def test_max_randomness_uses_expected_value():
    """
    Assert that :func:`~ulid.consts.MAX_RANDOMNESS` uses expected byte value.
    """
    value = consts.MAX_RANDOMNESS
    assert value == b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'


def test_min_ulid_uses_expected_value():
    """
    Assert that :func:`~ulid.consts.MIN_ULID` uses expected byte value.
    """
    value = consts.MIN_ULID
    assert value == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


def test_max_ulid_uses_expected_value():
    """
    Assert that :func:`~ulid.consts.MAX_ULID` uses expected byte value.
    """
    value = consts.MAX_ULID
    assert value == b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
