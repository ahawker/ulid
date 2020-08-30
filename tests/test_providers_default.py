"""
    test_providers_default
    ~~~~~~~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.providers.default` module.
"""
import time

import pytest

from ulid.providers import base, default


@pytest.fixture(scope='function')
def provider():
    """
    Fixture that yields a default provider instance.
    """
    return default.Provider()


def test_provider_derives_from_base():
    """
    Assert that :class:`~ulid.providers.default.Provider` derives from :class:`~ulid.providers.base.Provider`.
    """
    assert issubclass(default.Provider, base.Provider)


def test_provider_new_returns_bytes_pair(provider):
    """
    Assert that :meth:`~ulid.providers.default.Provider.new` returns timestamp and randomness
    bytes of expected length as a two item tuple.
    """
    value = provider.new()
    assert isinstance(value, tuple)
    assert len(value) == 2
    assert len(value[0]) == 6
    assert len(value[1]) == 10


def test_provider_timestamp_returns_bytes(provider):
    """
    Assert that :meth:`~ulid.providers.default.Provider.timestamp` returns bytes of expected length.
    """
    value = provider.timestamp()
    assert isinstance(value, bytes)
    assert len(value) == 6


def test_provider_timestamp_uses_time_epoch(provider):
    """
    Assert that :meth:`~ulid.providers.default.Provider.timestamp` returns the current time milliseconds
    since epoch in bytes.
    """
    timestamp_bytes = provider.timestamp()
    timestamp_int = int.from_bytes(timestamp_bytes, byteorder='big')
    assert timestamp_int // 1000 < time.time()


def test_provider_randomness_returns_bytes(provider):
    """
    Assert that :meth:`~ulid.providers.default.Provider.randomness` returns bytes of expected length.
    """
    value = provider.randomness(provider.timestamp())
    assert isinstance(value, bytes)
    assert len(value) == 10


def test_provider_randomness_returns_random_values_for_same_timestamp(provider):
    """
    Assert that :meth:`~ulid.providers.default.Provider.randomness` returns random bytes
    when given the same timestamp.
    """
    timestamp = provider.timestamp()
    x = provider.randomness(timestamp)
    y = provider.randomness(timestamp)

    assert x != y

    x_int = int.from_bytes(x, byteorder='big')
    y_int = int.from_bytes(y, byteorder='big')

    assert x_int + 1 != y_int
