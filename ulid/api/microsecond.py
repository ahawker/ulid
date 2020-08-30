"""
    ulid/api/microsecond
    ~~~~~~~~~~~~~~~~~~~~

    Contains the public API of the `ulid` package using the microsecond provider.
"""
from .. import consts, providers, ulid
from . import api

API = api.Api(providers.MICROSECOND)

create = API.create
from_bytes = API.from_bytes
from_int = API.from_int
from_randomness = API.from_randomness
from_str = API.from_str
from_timestamp = API.from_timestamp
from_uuid = API.from_uuid
new = API.new
parse = API.parse

MIN_TIMESTAMP = consts.MIN_TIMESTAMP
MAX_TIMESTAMP = consts.MAX_TIMESTAMP
MIN_RANDOMNESS = consts.MIN_RANDOMNESS
MAX_RANDOMNESS = consts.MAX_RANDOMNESS
MIN_ULID = consts.MIN_ULID
MAX_ULID = consts.MAX_ULID

Timestamp = ulid.Timestamp
Randomness = ulid.Randomness
ULID = ulid.ULID

__all__ = api.ALL
