"""
    ulid/ulid
    ~~~~~~~~~

    Object representation of a ULID.
"""
import datetime

from . import base32


__all__ = ['Timestamp', 'Randomness', 'ULID']


class MemoryView:
    """
    Wraps a buffer object, typically :class:`~bytes`, with a :class:`~memoryview` and provides easy
    type comparisons and conversions between presentation formats.
    """

    __slots__ = ['memory']

    def __init__(self, buffer):
        self.memory = memoryview(buffer)

    def __eq__(self, other):
        if isinstance(other, MemoryView):
            return self.memory == other.memory
        if isinstance(other, (bytes, bytearray, memoryview)):
            return self.memory == other
        if isinstance(other, int):
            return self.int == other
        if isinstance(other, str):
            return self.str == other
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, MemoryView):
            return self.memory != other.memory
        if isinstance(other, (bytes, bytearray, memoryview)):
            return self.memory != other
        if isinstance(other, int):
            return self.int != other
        if isinstance(other, str):
            return self.str != other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, MemoryView):
            return self.memory < other.memory
        if isinstance(other, (bytes, bytearray, memoryview)):
            return self.memory < other
        if isinstance(other, int):
            return self.int < other
        if isinstance(other, str):
            return self.str < other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, MemoryView):
            return self.memory > other.memory
        if isinstance(other, (bytes, bytearray, memoryview)):
            return self.memory > other
        if isinstance(other, int):
            return self.int > other
        if isinstance(other, str):
            return self.str > other
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, MemoryView):
            return self.memory <= other.memory
        if isinstance(other, (bytes, bytearray, memoryview)):
            return self.memory <= other
        if isinstance(other, int):
            return self.int <= other
        if isinstance(other, str):
            return self.str <= other
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, MemoryView):
            return self.memory >= other.memory
        if isinstance(other, (bytes, bytearray, memoryview)):
            return self.memory >= other
        if isinstance(other, int):
            return self.int >= other
        if isinstance(other, str):
            return self.str >= other
        return NotImplemented

    def __hash__(self):
        return hash(self.memory)

    def __int__(self):
        return self.int

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, str(self))

    def __str__(self):
        return self.str

    @property
    def bytes(self) -> bytes:
        """
        Computes the bytes value of the underlying :class:`~memoryview`.

        :return: Memory in bytes form
        :rtype: :class:`~bytes`
        """
        return self.memory.tobytes()

    @property
    def int(self) -> int:
        """
        Computes the integer value of the underlying :class:`~memoryview` in big-endian byte order.

        :return: Bytes in integer form.
        :rtype: :class:`~int`
        """
        return int.from_bytes(self.memory, byteorder='big')

    @property
    def str(self) -> str:
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
    def str(self) -> str:
        """
        Computes the string value of the timestamp from the underlying :class:`~memoryview` in Base32 encoding.

        :return: Timestamp in Base32 string form.
        :rtype: :class:`~str`
        :raises ValueError: if underlying :class:`~memoryview` cannot be encoded
        """
        return base32.encode_timestamp(self.memory)

    @property
    def timestamp(self):
        """
        Computes the Unix time (seconds since epoch) from its :class:`~memoryview`.

        :return: Timestamp in Unix time (seconds since epoch) form.
        :rtype: :class:`~int`
        """
        return self.int / 1000.0

    def datetime(self):
        """
        Creates a :class:`~datetime.datetime` instance (assumes UTC) from the Unix time value of the timestamp.

        :return: Timestamp in datetime form.
        :rtype: :class:`~datetime.datetime`
        """
        return datetime.datetime.utcfromtimestamp(self.timestamp)


class Randomness(MemoryView):
    """
    Represents the randomness portion of a ULID.

    * Cryptographically secure random values.
    * Last 80 bits of ULID when in binary format.
    * Last 16 characters of ULID when in string format.
    """

    __slots__ = MemoryView.__slots__

    @property
    def str(self) -> str:
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

    0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                      32_bit_uint_time_high                    |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |     16_bit_uint_time_low      |       16_bit_uint_random      |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                       32_bit_uint_random                      |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                       32_bit_uint_random                      |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """

    __slots__ = MemoryView.__slots__

    @property
    def str(self) -> str:
        """
        Computes the string value of the ULID from its :class:`~memoryview` in Base32 encoding.

        :return: ULID in Base32 string form.
        :rtype: :class:`~str`
        :raises ValueError: if underlying :class:`~memoryview` cannot be encoded
        """
        return base32.encode_ulid(self.memory)

    def timestamp(self):
        """
        Creates a :class:`~ulid.ulid.Timestamp` instance that maps to the first 48 bits of this ULID.

        :return: Timestamp from first 48 bits.
        :rtype: :class:`~ulid.ulid.Timestamp`
        """
        return Timestamp(self.memory[:6])

    def randomness(self):
        """
        Creates a :class:`~ulid.ulid.Randomness` instance that maps to the last 80 bits of this ULID.

        :return: Timestamp from first 48 bits.
        :rtype: :class:`~ulid.ulid.Timestamp`
        """
        return Randomness(self.memory[6:])
