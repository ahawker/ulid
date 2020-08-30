"""
    test_api_monotonic
    ~~~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.api.monotonic` module.
"""
from ulid.api import monotonic
from ulid.api.api import ALL


def test_module_has_dunder_all():
    """
    Assert that :mod:`~ulid.api.monotonic` exposes the :attr:`~ulid.api.__all__` attribute as a list.
    """
    assert hasattr(monotonic, '__all__')
    assert isinstance(monotonic.__all__, list)


def test_module_exposes_expected_interface():
    """
    Assert that :attr:`~ulid.api.monotonic.__all__` exposes expected interface.
    """
    assert monotonic.__all__ == ALL


def test_module_api_uses_correct_provider():
    """
    Assert that the API instance uses the correct provider type.
    """
    assert isinstance(monotonic.API.provider, type(monotonic.providers.MONOTONIC))
