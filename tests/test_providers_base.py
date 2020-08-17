"""
    test_providers_base
    ~~~~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.providers.base` module.
"""
import inspect

from ulid.providers import base


def test_provider_is_abstract():
    """
    Assert that :class:`~ulid.providers.base.Provider` is an abstract class.
    """
    assert inspect.isabstract(base.Provider)
