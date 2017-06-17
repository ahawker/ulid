"""
    ulid/hints
    ~~~~~~~~~~

    Contains type hint definitions across modules in the package.
"""
import typing


#: Type hint that defines multiple types that implement the buffer protocol
#: that can encoded into a Base32 string.
Buffer = typing.Union[bytes, bytearray, memoryview]
