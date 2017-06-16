"""
    ulid/hints
    ~~~~~~~~~~

    Contains type hint definitions for the package.
"""
import datetime
import typing


#: Type hint that defines multiple types that implement the buffer protocol
#: that can encoded into a Base32 string.
Buffer = typing.Union[bytes, bytearray, memoryview]


#: Type hint that defines multiple primitive types that can represent
#: a Unix timestamp in seconds.
TimestampPrimitive = typing.Union[int, float, str, bytes, bytearray, memoryview, datetime.datetime]


#: Type hint that defines multiple primitive types that can represent
#: randomness.
RandomnessPrimitive = typing.Union[int, float, str, bytes, bytearray, memoryview]
