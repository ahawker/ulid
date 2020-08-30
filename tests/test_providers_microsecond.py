"""
    test_providers_microsecond
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.providers.microsecond` module.
"""
import pytest

from ulid.providers import base, default, microsecond, time


@pytest.fixture(scope='function')
def provider():
    """
    Fixture that yields a microsecond provider instance.
    """
    return microsecond.Provider(default.Provider())


@pytest.fixture(scope='function')
def valid_epoch_milliseconds():
    """
    Fixture that yields a epoch value in milliseconds.
    """
    return time.PROVIDER.milliseconds()


@pytest.fixture(scope='function')
def valid_epoch_microseconds():
    """
    Fixture that yields a epoch value in microseconds.
    """
    return time.PROVIDER.microseconds()


@pytest.fixture(scope='function')
def mock_time_provider(mocker, valid_epoch_milliseconds, valid_epoch_microseconds):
    """
    Fixture that yields a mock time provider.
    """
    provider = mocker.Mock(spec=time.Provider)
    provider.milliseconds = mocker.Mock(return_value=valid_epoch_milliseconds)
    provider.microseconds = mocker.Mock(return_value=valid_epoch_microseconds)
    return provider


@pytest.fixture(scope='function')
def provider_time_mock(mocker, mock_time_provider):
    """
    Fixture that yields a provider with time mock.
    """
    mocker.patch.object(microsecond.time, 'milliseconds', side_effect=mock_time_provider.milliseconds)
    mocker.patch.object(microsecond.time, 'microseconds', side_effect=mock_time_provider.microseconds)
    return microsecond.Provider(default.Provider())


def test_provider_derives_from_base():
    """
    Assert that :class:`~ulid.providers.microsecond.Provider` derives from :class:`~ulid.providers.base.Provider`.
    """
    assert issubclass(microsecond.Provider, base.Provider)


def test_provider_new_returns_bytes_pair(provider):
    """
    Assert that :meth:`~ulid.providers.microsecond.Provider.new` returns timestamp and randomness
    bytes of expected length as a two item tuple.
    """
    value = provider.new()
    assert isinstance(value, tuple)
    assert len(value) == 2
    assert len(value[0]) == 6
    assert len(value[1]) == 10


def test_provider_new_returns_randomness_with_microseconds(provider_time_mock):
    """
    Assert that :meth:`~ulid.providers.default.Provider.new` returns timestamp and randomness
    bytes that use microseconds as the first two bytes of randomness.
    """
    epoch_us = time.microseconds()
    epoch_ms = epoch_us // 1000
    microseconds = epoch_us % epoch_ms
    microseconds_bits = microseconds << 6

    _, randomness = provider_time_mock.new()

    prefix = int.from_bytes(randomness[:2], byteorder='big')
    microsecond_prefix_bits = (prefix >> 6) << 6

    assert microsecond_prefix_bits == microseconds_bits


def test_provider_timestamp_returns_bytes(provider):
    """
    Assert that :meth:`~ulid.providers.microsecond.Provider.timestamp` returns bytes of expected length.
    """
    value = provider.timestamp()
    assert isinstance(value, bytes)
    assert len(value) == 6


def test_provider_timestamp_uses_time_epoch(provider):
    """
    Assert that :meth:`~ulid.providers.microsecond.Provider.timestamp` returns the current time milliseconds
    since epoch in bytes.
    """
    timestamp_bytes = provider.timestamp()
    timestamp_int = int.from_bytes(timestamp_bytes, byteorder='big')
    assert timestamp_int <= time.milliseconds()


def test_provider_randomness_returns_bytes(provider):
    """
    Assert that :meth:`~ulid.providers.microsecond.Provider.randomness` returns bytes of expected length.
    """
    value = provider.randomness(provider.timestamp())
    assert isinstance(value, bytes)
    assert len(value) == 10
