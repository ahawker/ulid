"""
    test_api_default
    ~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.api.default` module.
"""
from ulid.api import default
from ulid.api.api import ALL


def test_module_has_dunder_all():
    """
    Assert that :mod:`~ulid.api.default` exposes the :attr:`~ulid.api.__all__` attribute as a list.
    """
    assert hasattr(default, '__all__')
    assert isinstance(default.__all__, list)


def test_module_exposes_expected_interface():
    """
    Assert that :attr:`~ulid.api.default.__all__` exposes expected interface.
    """
    assert default.__all__ == ALL
