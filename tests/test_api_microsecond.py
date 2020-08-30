"""
    test_api_microsecond
    ~~~~~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.api.microsecond` module.
"""
from ulid.api import microsecond
from ulid.api.api import ALL


def test_module_has_dunder_all():
    """
    Assert that :mod:`~ulid.api.microsecond` exposes the :attr:`~ulid.api.__all__` attribute as a list.
    """
    assert hasattr(microsecond, '__all__')
    assert isinstance(microsecond.__all__, list)


def test_module_exposes_expected_interface():
    """
    Assert that :attr:`~ulid.api.microsecond.__all__` exposes expected interface.
    """
    assert microsecond.__all__ == ALL


def test_module_api_uses_correct_provider():
    """
    Assert that the API instance uses the correct provider type.
    """
    assert isinstance(microsecond.API.provider, type(microsecond.providers.MICROSECOND))
