"""
    ulid/ulid
    ~~~~~~~~~

    Object representation of a ULID.
"""
import datetime
import typing
import uuid

from . import base32, hints

__all__ = ['Timestamp', 'Randomness', 'ULID']


#: Type hint that defines multiple primitive types and itself for comparing MemoryView instances.
MemoryViewPrimitive = typing.Union['MemoryView', hints.Primitive]  # pylint: disable=invalid-name


class MemoryView:
    """
    Wraps a buffer object, typically :class:`~bytes`, with a :class:`~memoryview` and provides easy
    type comparisons and conversions between presentation formats.
    """

    __slots__ = ['memory']

    def __init__(self, buffer: hints.Buffer) -> None:
        self.memory = memoryview(buffer)

    def __eq__(self, other: MemoryViewPrimitive) -> hints.Bool:  # type: ignore[override]
        if isinstance(other, MemoryView):
            return self.memory == other.memory
        if isinstance(other, (bytes, bytearray, memoryview)):
            return self.memory == other
        if isinstance(other, int):
            return self.int == other
        if isinstance(other, float):
            return self.float == other
        if isinstance(other, str):
            return self.str == other
        return NotImplemented

    def __ne__(self, other: MemoryViewPrimitive) -> hints.Bool:  # type: ignore[override]
        if isinstance(other, MemoryView):
            return self.memory != other.memory
        if isinstance(other, (bytes, bytearray, memoryview)):
            return self.memory != other
        if isinstance(other, int):
            return self.int != other
        if isinstance(other, float):
            return self.float != other
        if isinstance(other, str):
            return self.str != other
        return NotImplemented

    def __lt__(self, other: MemoryViewPrimitive) -> hints.Bool:
        if isinstance(other, MemoryView):
            return self.int < other.int
        if isinstance(other, (bytes, bytearray)):
            return self.bytes < other
        if isinstance(other, memoryview):
            return self.bytes < other.tobytes()
        if isinstance(other, int):
            return self.int < other
        if isinstance(other, float):
            return self.float < other
        if isinstance(other, str):
            return self.str < other
        return NotImplemented

    def __gt__(self, other: MemoryViewPrimitive) -> hints.Bool:
        if isinstance(other, MemoryView):
            return self.int > other.int
        if isinstance(other, (bytes, bytearray)):
            return self.bytes > other
        if isinstance(other, memoryview):
            return self.bytes > other.tobytes()
        if isinstance(other, int):
            return self.int > other
        if isinstance(other, float):
            return self.float > other
        if isinstance(other, str):
            return self.str > other
        return NotImplemented

    def __le__(self, other: MemoryViewPrimitive) -> hints.Bool:
        if isinstance(other, MemoryView):
            return self.int <= other.int
        if isinstance(other, (bytes, bytearray)):
            return self.bytes <= other
        if isinstance(other, memoryview):
            return self.bytes <= other.tobytes()
        if isinstance(other, int):
            return self.int <= other
        if isinstance(other, float):
            return self.float <= other
        if isinstance(other, str):
            return self.str <= other
        return NotImplemented

    def __ge__(self, other: MemoryViewPrimitive) -> hints.Bool:
        if isinstance(other, MemoryView):
            return self.int >= other.int
        if isinstance(other, (bytes, bytearray)):
            return self.bytes >= other
        if isinstance(other, memoryview):
            return self.bytes >= other.tobytes()
        if isinstance(other, int):
            return self.int >= other
        if isinstance(other, float):
            return self.float >= other
        if isinstance(other, str):
            return self.str >= other
        return NotImplemented

    def __hash__(self) -> hints.Int:
        return hash(self.memory)

    def __bytes__(self) -> hints.Bytes:
        return self.bytes

    def __float__(self) -> hints.Float:
        return self.float

    def __int__(self) -> hints.Int:
        return self.int

    def __index__(self) -> hints.Int:
        return self.int

    def __repr__(self) -> hints.Str:
        return '<{}({!r})>'.format(self.__class__.__name__, str(self))

    def __str__(self) -> hints.Str:
        return self.str

    def __getstate__(self) -> hints.Str:
        return self.str

    def __setstate__(self, state: hints.Str) -> None:
        self.memory = memoryview(base32.decode(state))

    @property
    def bin(self) -> hints.Str:
        """
        Computes the binary string value of the underlying :class:`~memoryview`.

        :return: Memory in binary string form
        :rtype: :class:`~str`
        """
        return bin(self.int)

    @property
    def bytes(self) -> hints.Bytes:
        """
        Computes the bytes value of the underlying :class:`~memoryview`.

        :return: Memory in bytes form
        :rtype: :class:`~bytes`
        """
        return self.memory.tobytes()

    @property
    def float(self) -> hints.Float:
        """
        Computes the float value of the underlying :class:`~memoryview` in big-endian byte order.

        :return: Bytes in float form.
        :rtype: :class:`~float`
        """
        return float(self.int)

    @property
    def hex(self) -> hints.Str:
        """
        Computes the hexadecimal string value of the underlying :class:`~memoryview`.

        :return: Memory in hexadecimal string form
        :rtype: :class:`~str`
        """
        return hex(self.int)

    @property
    def int(self) -> hints.Int:
        """
        Computes the integer value of the underlying :class:`~memoryview` in big-endian byte order.

        :return: Bytes in integer form.
        :rtype: :class:`~int`
        """
        return int.from_bytes(self.memory, byteorder='big')

    @property
    def oct(self) -> hints.Str:
        """
        Computes the octal string value of the underlying :class:`~memoryview`.

        :return: Memory in octal string form
        :rtype: :class:`~str`
        """
        return oct(self.int)

    @property
    def str(self) -> hints.Str:
        """
        Computes the string value of the underlying :class:`~memoryview` in Base32 encoding.

        .. note:: The base implementation here will call :func:`~ulid.base32.encode` which
        performs analysis on the bytes to determine how it should be decoded. This is going to
        be slightly slower than calling the explicit `encode_*` methods so each model that
        derives from this class can/should override and specify the explicit function to call.

        :return: Bytes in Base32 string form.
        :rtype: :class:`~str`
        :raises ValueError: if underlying :class:`~memoryview` cannot be encoded
        """
        return base32.encode(self.memory)


class Timestamp(MemoryView):
    """
    Represents the timestamp portion of a ULID.

    * Unix time (time since epoch) in milliseconds.
    * First 48 bits of ULID when in binary format.
    * First 10 characters of ULID when in string format.
    """

    __slots__ = MemoryView.__slots__

    @property
    def str(self) -> hints.Str:
        """
        Computes the string value of the timestamp from the underlying :class:`~memoryview` in Base32 encoding.

        :return: Timestamp in Base32 string form.
        :rtype: :class:`~str`
        :raises ValueError: if underlying :class:`~memoryview` cannot be encoded
        """
        return base32.encode_timestamp(self.memory)

    @property
    def timestamp(self) -> hints.Float:
        """
        Computes the Unix time (seconds since epoch) from its :class:`~memoryview`.

        :return: Timestamp in Unix time (seconds since epoch) form.
        :rtype: :class:`~float`
        """
        return self.int / 1000.0

    @property
    def datetime(self) -> hints.Datetime:
        """
        Creates a :class:`~datetime.datetime` instance (assumes UTC) from the Unix time value of the timestamp
        with millisecond precision.

        :return: Timestamp in datetime form.
        :rtype: :class:`~datetime.datetime`
        """
        milli = self.int
        micro = milli % 1000 * 1000
        sec = milli // 1000.0
        timezone = datetime.timezone.utc

        return datetime.datetime.utcfromtimestamp(sec).replace(microsecond=micro, tzinfo=timezone)


class Randomness(MemoryView):
    """
    Represents the randomness portion of a ULID.

    * Cryptographically secure random values.
    * Last 80 bits of ULID when in binary format.
    * Last 16 characters of ULID when in string format.
    """

    __slots__ = MemoryView.__slots__

    @property
    def str(self) -> hints.Str:
        """
        Computes the string value of the randomness from the underlying :class:`~memoryview` in Base32 encoding.

        :return: Timestamp in Base32 string form.
        :rtype: :class:`~str`
        :raises ValueError: if underlying :class:`~memoryview` cannot be encoded
        """
        return base32.encode_randomness(self.memory)


class ULID(MemoryView):
    """
    Represents a ULID.

    * 128 bits in binary format.
    * 26 characters in string format.
    * 16 octets.
    * Network byte order, big-endian, most significant bit first.
    """

    __slots__ = MemoryView.__slots__

    @property
    def str(self) -> hints.Str:
        """
        Computes the string value of the ULID from its :class:`~memoryview` in Base32 encoding.

        :return: ULID in Base32 string form.
        :rtype: :class:`~str`
        :raises ValueError: if underlying :class:`~memoryview` cannot be encoded
        """
        return base32.encode_ulid(self.memory)

    def timestamp(self) -> Timestamp:
        """
        Creates a :class:`~ulid.ulid.Timestamp` instance that maps to the first 48 bits of this ULID.

        :return: Timestamp from first 48 bits.
        :rtype: :class:`~ulid.ulid.Timestamp`
        """
        return Timestamp(self.memory[:6])

    def randomness(self) -> Randomness:
        """
        Creates a :class:`~ulid.ulid.Randomness` instance that maps to the last 80 bits of this ULID.

        :return: Timestamp from first 48 bits.
        :rtype: :class:`~ulid.ulid.Timestamp`
        """
        return Randomness(self.memory[6:])

    @property
    def uuid(self) -> hints.UUID:
        """
        Creates a :class:`~uuid.UUID` instance of the ULID from its :class:`~bytes` representation.

        :return: UUIDv4 from the ULID bytes
        :rtype: :class:`~uuid.UUID`
        """
        return uuid.UUID(bytes=self.bytes)
