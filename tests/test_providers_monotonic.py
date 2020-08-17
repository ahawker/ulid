"""
    test_providers_monotonic
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.providers.monotonic` module.
"""
import time

import pytest

from ulid.providers import base, default, monotonic

RANDOMNESS_OVERFLOW_REGEX = r'^Monotonic randomness value too large and will overflow'


@pytest.fixture(scope='function')
def provider():
    """
    Fixture that yields a monotonic provider instance.
    """
    return monotonic.Provider(default.Provider())


def test_provider_derives_from_base():
    """
    Assert that :class:`~ulid.providers.monotonic.Provider` derives from :class:`~ulid.providers.base.Provider`.
    """
    assert issubclass(monotonic.Provider, base.Provider)


def test_provider_timestamp_returns_bytes(provider):
    """
    Assert that :meth:`~ulid.providers.monotonic.Provider.timestamp` returns bytes of expected length.
    """
    value = provider.timestamp()
    assert isinstance(value, bytes)
    assert len(value) == 6


def test_provider_timestamp_uses_time_epoch(provider):
    """
    Assert that :meth:`~ulid.providers.monotonic.Provider.timestamp` returns the current time milliseconds
    since epoch in bytes.
    """
    timestamp_bytes = provider.timestamp()
    timestamp_int = int.from_bytes(timestamp_bytes, byteorder='big')
    assert timestamp_int // 1000 < time.time()


def test_provider_randomness_returns_bytes(provider):
    """
    Assert that :meth:`~ulid.providers.monotonic.Provider.randomness` returns bytes of expected length.
    """
    value = provider.randomness(provider.timestamp())
    assert isinstance(value, bytes)
    assert len(value) == 10


def test_provider_randomness_returns_increasing_values_for_same_timestamp(provider):
    """
    Assert that :meth:`~ulid.providers.monotonic.Provider.randomness` returns incremented random values
    for matching timestamps.
    """
    timestamp = provider.timestamp()
    x = provider.randomness(timestamp)
    y = provider.randomness(timestamp)

    assert x != y

    x_int = int.from_bytes(x, byteorder='big')
    y_int = int.from_bytes(y, byteorder='big')

    assert x_int + 1 == y_int


def test_provider_randomness_raises_on_max_randomness(provider):
    """
    Assert that :meth:`~ulid.providers.monotonic.Provider.randomness` raises a :class:`~ValueError`
    when incrementing the randomness value for the same timestamp would overflow.
    """
    timestamp = provider.timestamp()

    with pytest.raises(ValueError, match=RANDOMNESS_OVERFLOW_REGEX):
        provider.randomness(timestamp)
        provider.prev_randomness = monotonic.consts.MAX_RANDOMNESS
        provider.randomness(timestamp)
