"""
    test_providers_time_base
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for the :mod:`~ulid.providers.time.base` module.
"""
import inspect

from ulid.providers.time import base


def test_provider_is_abstract():
    """
    Assert that :class:`~ulid.providers.time.base.Provider` is an abstract class.
    """
    assert inspect.isabstract(base.Provider)
