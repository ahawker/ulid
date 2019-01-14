"""
    test_module
    ~~~~~~~~~~~

    Tests for the :mod:`~ulid` module.
"""
import pytest

import ulid as mod
from ulid import api, ulid


def test_module_has_dunder_version():
    """
    Assert that :mod:`~ulid` exposes the :attr:`~ulid.__version__` attribute as a string.
    """
    assert hasattr(mod, '__version__')
    assert isinstance(mod.__version__, str)


def test_module_has_dunder_all():
    """
    Assert that :mod:`~ulid` exposes the :attr:`~ulid.__all__` attribute as a list.
    """
    assert hasattr(mod, '__all__')
    assert isinstance(mod.__all__, list)


@pytest.mark.parametrize('submodule', [api, ulid])
def test_module_has_submodule_interface(submodule):
    """
    Assert that :mod:`~ulid` exposes the given submodules `__all__` attribute from an import
    so it's in scope.
    """
    assert hasattr(submodule, '__all__')
    for i in submodule.__all__:
        assert hasattr(mod, i)


def test_module_exposes_api_and_ulid_interfaces_via_all():
    """
    Assert that :mod:`~ulid` exposes the :attr:`~ulid.api.__all__` and :attr:`~ulid.ulid.__all__`
    attributes in its public interface.
    """
    assert mod.__all__ == api.__all__ + ulid.__all__
