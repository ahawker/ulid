"""
    ulid/providers
    ~~~~~~~~~~~~~~

    Contains functionality for timestamp/randomness data providers.
"""

from . import base, default, microsecond, monotonic

Provider = base.Provider
DEFAULT = default.Provider()
MICROSECOND = microsecond.Provider(DEFAULT)
MONOTONIC = monotonic.Provider(DEFAULT)

__all__ = ['Provider', 'DEFAULT', 'MICROSECOND', 'MONOTONIC']
