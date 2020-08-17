"""
    ulid/hints
    ~~~~~~~~~~

    Contains type hint definitions across modules in the package.
"""
import datetime
import types
import typing
import uuid

#: Type hint that is an alias for the built-in :class:`~bool` type.
Bool = bool

#: Type hint that defines multiple types that implement the buffer protocol
#: that can encoded into a Base32 string.
Buffer = typing.Union[bytes, bytearray, memoryview]  # pylint: disable=invalid-name


#: Type hint that is an alias for the built-in :class:`~bytes` type.
Bytes = bytes  # pylint: disable=invalid-name


#: Type hint that is an alias for the built-in :class:`~datetime.datetime` type.
Datetime = datetime.datetime  # pylint: disable=invalid-name


#: Type hint that is an alias for the built-in :class:`~float` type.
Float = float  # pylint: disable=invalid-name


#: Type hint that is an alias for the built-in :class:`~int` type.
Int = int  # pylint: disable=invalid-name


#: Type hint that is an alias for the built-in :class:`~types.ModuleType` type.
Module = types.ModuleType


#: Type hint that defines multiple primitive types that can represent parts or full ULID.
Primitive = typing.Union[int, float, str, bytes, bytearray, memoryview]  # pylint: disable=invalid-name


#: Type hint that is an alias for the built-in :class:`~str` type.
Str = str  # pylint: disable=invalid-name


#: Type hint that is an alias for the built-in :class:`~datetime.datetime` type.
UUID = uuid.UUID  # pylint: disable=invalid-name
