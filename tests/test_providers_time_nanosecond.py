"""
    test_providers_time_default
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.providers.time.default` module.
"""
import sys
import time

import pytest

from ulid.providers.time import base, nanosecond

pytestmark = pytest.mark.skipif(sys.version_info < (3, 7), reason="Requires py3.7+ for time.time_ns()")


@pytest.fixture(scope='function')
def provider():
    """
    Fixture that yields a time provider instance.
    """
    return nanosecond.Provider()


def test_provider_derives_from_base():
    """
    Assert that :class:`~ulid.providers.time.nanosecond.Provider` derives
    from :class:`~ulid.providers.time.base.Provider`.
    """
    assert issubclass(nanosecond.Provider, base.Provider)


def test_provider_milliseconds_returns_int(provider):
    """
    Assert that :meth:`~ulid.providers.time.nanosecond.Provider.milliseconds` returns :class:`~int`.
    """
    value = provider.milliseconds()
    assert isinstance(value, int)


def test_provider_microseconds_returns_int(provider):
    """
    Assert that :meth:`~ulid.providers.time.nanosecond.Provider.microseconds` returns :class:`~int`.
    """
    value = provider.microseconds()
    assert isinstance(value, int)


def test_provider_milliseconds_is_unix_epoch(provider):
    """
    Assert that :meth:`~ulid.providers.time.nanosecond.Provider.milliseconds` returns the current time milliseconds
    since epoch.
    """
    x = int(time.time() * 1000)
    y = provider.milliseconds()
    z = int(time.time() * 1000)

    assert x <= y <= z


def test_provider_microseconds_is_unix_epoch(provider):
    """
    Assert that :meth:`~ulid.providers.time.nanosecond.Provider.microseconds` returns the current time microseconds
    since epoch.
    """
    x = int(time.time() * 1000 * 1000)
    y = provider.microseconds()
    z = int(time.time() * 1000 * 1000)

    assert x <= y <= z
