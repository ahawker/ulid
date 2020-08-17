"""
    ulid/consts
    ~~~~~~~~~~~

    Contains public API constant values.
"""
from . import ulid

__all__ = ['MIN_TIMESTAMP', 'MAX_TIMESTAMP', 'MIN_RANDOMNESS', 'MAX_RANDOMNESS', 'MIN_ULID', 'MAX_ULID']

#: Minimum possible timestamp value (0).
MIN_TIMESTAMP = ulid.Timestamp(b'\x00\x00\x00\x00\x00\x00')


#: Maximum possible timestamp value (281474976710.655 epoch).
MAX_TIMESTAMP = ulid.Timestamp(b'\xff\xff\xff\xff\xff\xff')


#: Minimum possible randomness value (0).
MIN_RANDOMNESS = ulid.Randomness(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')


#: Maximum possible randomness value (1208925819614629174706175).
MAX_RANDOMNESS = ulid.Randomness(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')


#: Minimum possible ULID value (0).
MIN_ULID = ulid.ULID(MIN_TIMESTAMP.bytes + MIN_RANDOMNESS.bytes)


#: Maximum possible ULID value (340282366920938463463374607431768211455).
MAX_ULID = ulid.ULID(MAX_TIMESTAMP.bytes + MAX_RANDOMNESS.bytes)
