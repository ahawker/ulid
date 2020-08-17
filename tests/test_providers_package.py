"""
    test_providers_package
    ~~~~~~~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.providers` package.
"""
from ulid import providers
from ulid.providers import default, monotonic


def test_package_has_dunder_all():
    """
    Assert that :pkg:`~ulid.providers` exposes the :attr:`~ulid.providers.__all__` attribute as a list.
    """
    assert hasattr(providers, '__all__')
    assert isinstance(providers.__all__, list)


def test_package_exposes_expected_interface():
    """
    Assert that :attr:`~ulid.providers.__all__` exposes expected interface.
    """
    assert providers.__all__ == ['Provider', 'DEFAULT', 'MONOTONIC']


def test_package_has_default_provider():
    """
    Assert :attr:`~ulid.providers.DEFAULT` is a :class:`~ulid.providers.default.Provider` instance.
    """
    assert isinstance(providers.DEFAULT, default.Provider)


def test_package_has_monotonic_provider():
    """
    Assert :attr:`~ulid.providers.MONOTONIC` is a :class:`~ulid.providers.monotonic.Provider` instance.
    """
    assert isinstance(providers.MONOTONIC, monotonic.Provider)
