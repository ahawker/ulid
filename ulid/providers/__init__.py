"""
    ulid/providers
    ~~~~~~~~~~~~~~

    Contains functionality for timestamp/randomness data providers.
"""

from . import base, default, monotonic

Provider = base.Provider
DEFAULT = default.Provider()
MONOTONIC = monotonic.Provider(DEFAULT)

__all__ = ['Provider', 'DEFAULT', 'MONOTONIC']
