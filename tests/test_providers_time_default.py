"""
    test_providers_time_default
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.providers.time.default` module.
"""
import time

import pytest

from ulid.providers.time import base, default


@pytest.fixture(scope='function')
def provider():
    """
    Fixture that yields a time provider instance.
    """
    return default.Provider()


def test_provider_derives_from_base():
    """
    Assert that :class:`~ulid.providers.time.default.Provider` derives from :class:`~ulid.providers.time.base.Provider`.
    """
    assert issubclass(default.Provider, base.Provider)


def test_provider_milliseconds_returns_int(provider):
    """
    Assert that :meth:`~ulid.providers.time.default.Provider.milliseconds` returns :class:`~int`.
    """
    value = provider.milliseconds()
    assert isinstance(value, int)


def test_provider_microseconds_returns_int(provider):
    """
    Assert that :meth:`~ulid.providers.time.default.Provider.microseconds` returns :class:`~int`.
    """
    value = provider.microseconds()
    assert isinstance(value, int)


def test_provider_milliseconds_is_unix_epoch(provider):
    """
    Assert that :meth:`~ulid.providers.time.default.Provider.milliseconds` returns the current time milliseconds
    since epoch.
    """
    x = int(time.time() * 1000)
    time.sleep(1)
    y = provider.milliseconds()
    time.sleep(1)
    z = int(time.time() * 1000)

    assert x <= y <= z


def test_provider_microseconds_is_unix_epoch(provider):
    """
    Assert that :meth:`~ulid.providers.time.default.Provider.microseconds` returns the current time microseconds
    since epoch.
    """
    x = int(time.time() * 1000 * 1000)
    time.sleep(1)
    y = provider.microseconds()
    time.sleep(1)
    z = int(time.time() * 1000 * 1000)

    assert x <= y <= z
