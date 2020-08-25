"""
    ulid/base32
    ~~~~~~~~~~~

    Functionality for encoding/decoding ULID strings/bytes using Base32 format.

    .. note:: This module makes the trade-off of code duplication for inline
        computations over multiple function calls for performance reasons. I'll
        check metrics in the future to see how much it helps and if it's worth
        it to maintain.

    * `Base32 Documentation <http://www.crockford.com/wrmg/base32.html>`
    * `NUlid Project <https://github.com/RobThree/NUlid>`
"""
import array

from . import hints

#: Base32 character set. Excludes characters "I L O U".
ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


#: Array that maps encoded string char byte values to enable O(1) lookups.
DECODING = array.array(
    'B',
    (0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x01,
     0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E,
     0x0F, 0x10, 0x11, 0x01, 0x12, 0x13, 0x01, 0x14, 0x15, 0x00,
     0x16, 0x17, 0x18, 0x19, 0x1A, 0xFF, 0x1B, 0x1C, 0x1D, 0x1E,
     0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x0A, 0x0B, 0x0C,
     0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x01, 0x12, 0x13, 0x01, 0x14,
     0x15, 0x00, 0x16, 0x17, 0x18, 0x19, 0x1A, 0xFF, 0x1B, 0x1C,
     0x1D, 0x1E, 0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
     0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF)
)


def encode(value: hints.Buffer) -> str:
    """
    Encode the given :class:`~bytes` instance to a :class:`~str` using Base32 encoding.

    .. note:: You should only use this method if you've got a :class:`~bytes` instance
        and you are unsure of what it represents. If you know the the _meaning_ of the
        :class:`~bytes` instance, you should call the `encode_*` method explicitly for
        better performance.

    :param value: Bytes to encode
    :type value: :class:`~bytes`, :class:`~bytearray`, or :class:`~memoryview`
    :return: Value encoded as a Base32 string
    :rtype: :class:`~str`
    :raises ValueError: when the value is not 6, 10, or 16 bytes long
    """
    length = len(value)

    # Order here is based on assumed hot path.
    if length == 16:
        return encode_ulid(value)
    if length == 6:
        return encode_timestamp(value)
    if length == 10:
        return encode_randomness(value)

    raise ValueError('Expects bytes in sizes of 6, 10, or 16; got {}'.format(length))


def encode_ulid(value: hints.Buffer) -> str:
    """
    Encode the given buffer to a :class:`~str` using Base32 encoding.

    .. note:: This uses an optimized strategy from the `NUlid` project for encoding ULID
        bytes specifically and is not meant for arbitrary encoding.

    :param value: Bytes to encode
    :type value: :class:`~bytes`, :class:`~bytearray`, or :class:`~memoryview`
    :return: Value encoded as a Base32 string
    :rtype: :class:`~str`
    :raises ValueError: when the value is not 16 bytes
    """
    length = len(value)
    if length != 16:
        raise ValueError('Expects 16 bytes for timestamp + randomness; got {}'.format(length))

    encoding = ENCODING

    return \
        encoding[(value[0] & 224) >> 5] + \
        encoding[value[0] & 31] + \
        encoding[(value[1] & 248) >> 3] + \
        encoding[((value[1] & 7) << 2) | ((value[2] & 192) >> 6)] + \
        encoding[((value[2] & 62) >> 1)] + \
        encoding[((value[2] & 1) << 4) | ((value[3] & 240) >> 4)] + \
        encoding[((value[3] & 15) << 1) | ((value[4] & 128) >> 7)] + \
        encoding[(value[4] & 124) >> 2] + \
        encoding[((value[4] & 3) << 3) | ((value[5] & 224) >> 5)] + \
        encoding[value[5] & 31] + \
        encoding[(value[6] & 248) >> 3] + \
        encoding[((value[6] & 7) << 2) | ((value[7] & 192) >> 6)] + \
        encoding[(value[7] & 62) >> 1] + \
        encoding[((value[7] & 1) << 4) | ((value[8] & 240) >> 4)] + \
        encoding[((value[8] & 15) << 1) | ((value[9] & 128) >> 7)] + \
        encoding[(value[9] & 124) >> 2] + \
        encoding[((value[9] & 3) << 3) | ((value[10] & 224) >> 5)] + \
        encoding[value[10] & 31] + \
        encoding[(value[11] & 248) >> 3] + \
        encoding[((value[11] & 7) << 2) | ((value[12] & 192) >> 6)] + \
        encoding[(value[12] & 62) >> 1] + \
        encoding[((value[12] & 1) << 4) | ((value[13] & 240) >> 4)] + \
        encoding[((value[13] & 15) << 1) | ((value[14] & 128) >> 7)] + \
        encoding[(value[14] & 124) >> 2] + \
        encoding[((value[14] & 3) << 3) | ((value[15] & 224) >> 5)] + \
        encoding[value[15] & 31]


def encode_timestamp(timestamp: hints.Buffer) -> str:
    """
    Encode the given buffer to a :class:`~str` using Base32 encoding.

    The given :class:`~bytes` are expected to represent the first 6 bytes of a ULID, which
    are a timestamp in milliseconds.

    .. note:: This uses an optimized strategy from the `NUlid` project for encoding ULID
        bytes specifically and is not meant for arbitrary encoding.

    :param timestamp: Bytes to encode
    :type timestamp: :class:`~bytes`, :class:`~bytearray`, or :class:`~memoryview`
    :return: Value encoded as a Base32 string
    :rtype: :class:`~str`
    :raises ValueError: when the timestamp is not 6 bytes
    """
    length = len(timestamp)
    if length != 6:
        raise ValueError('Expects 6 bytes for timestamp; got {}'.format(length))

    encoding = ENCODING

    return \
        encoding[(timestamp[0] & 224) >> 5] + \
        encoding[timestamp[0] & 31] + \
        encoding[(timestamp[1] & 248) >> 3] + \
        encoding[((timestamp[1] & 7) << 2) | ((timestamp[2] & 192) >> 6)] + \
        encoding[((timestamp[2] & 62) >> 1)] + \
        encoding[((timestamp[2] & 1) << 4) | ((timestamp[3] & 240) >> 4)] + \
        encoding[((timestamp[3] & 15) << 1) | ((timestamp[4] & 128) >> 7)] + \
        encoding[(timestamp[4] & 124) >> 2] + \
        encoding[((timestamp[4] & 3) << 3) | ((timestamp[5] & 224) >> 5)] + \
        encoding[timestamp[5] & 31]


def encode_randomness(randomness: hints.Buffer) -> str:
    """
    Encode the given buffer to a :class:`~str` using Base32 encoding.

    The given :class:`~bytes` are expected to represent the last 10 bytes of a ULID, which
    are cryptographically secure random values.

    .. note:: This uses an optimized strategy from the `NUlid` project for encoding ULID
        bytes specifically and is not meant for arbitrary encoding.

    :param randomness: Bytes to encode
    :type randomness: :class:`~bytes`, :class:`~bytearray`, or :class:`~memoryview`
    :return: Value encoded as a Base32 string
    :rtype: :class:`~str`
    :raises ValueError: when the randomness is not 10 bytes
    """
    length = len(randomness)
    if length != 10:
        raise ValueError('Expects 10 bytes for randomness; got {}'.format(length))

    encoding = ENCODING

    return \
        encoding[(randomness[0] & 248) >> 3] + \
        encoding[((randomness[0] & 7) << 2) | ((randomness[1] & 192) >> 6)] + \
        encoding[(randomness[1] & 62) >> 1] + \
        encoding[((randomness[1] & 1) << 4) | ((randomness[2] & 240) >> 4)] + \
        encoding[((randomness[2] & 15) << 1) | ((randomness[3] & 128) >> 7)] + \
        encoding[(randomness[3] & 124) >> 2] + \
        encoding[((randomness[3] & 3) << 3) | ((randomness[4] & 224) >> 5)] + \
        encoding[randomness[4] & 31] + \
        encoding[(randomness[5] & 248) >> 3] + \
        encoding[((randomness[5] & 7) << 2) | ((randomness[6] & 192) >> 6)] + \
        encoding[(randomness[6] & 62) >> 1] + \
        encoding[((randomness[6] & 1) << 4) | ((randomness[7] & 240) >> 4)] + \
        encoding[((randomness[7] & 15) << 1) | ((randomness[8] & 128) >> 7)] + \
        encoding[(randomness[8] & 124) >> 2] + \
        encoding[((randomness[8] & 3) << 3) | ((randomness[9] & 224) >> 5)] + \
        encoding[randomness[9] & 31]


def decode(value: str) -> bytes:
    """
    Decode the given Base32 encoded :class:`~str` instance to :class:`~bytes`.

    .. note:: You should only use this method if you've got a :class:`~str` instance
        and you are unsure of what it represents. If you know the the _meaning_ of the
        :class:`~str` instance, you should call the `decode_*` method explicitly for
        better performance.

    :param value: String to decode
    :type value: :class:`~str`
    :return: Value decoded from Base32 string
    :rtype: :class:`~bytes`
    :raises ValueError: when value is not 10, 16, or 26 characters
    :raises ValueError: when value cannot be encoded in ASCII
    """
    length = len(value)

    # Order here is based on assumed hot path.
    if length == 26:
        return decode_ulid(value)
    if length == 10:
        return decode_timestamp(value)
    if length == 16:
        return decode_randomness(value)

    raise ValueError('Expects string in lengths of 10, 16, or 26; got {}'.format(length))


def decode_ulid(value: str) -> bytes:
    """
    Decode the given Base32 encoded :class:`~str` instance to :class:`~bytes`.

    .. note:: This uses an optimized strategy from the `NUlid` project for decoding ULID
        strings specifically and is not meant for arbitrary decoding.


    :param value: String to decode
    :type value: :class:`~str`
    :return: Value decoded from Base32 string
    :rtype: :class:`~bytes`
    :raises ValueError: when value is not 26 characters
    :raises ValueError: when value cannot be encoded in ASCII
    """
    encoded = str_to_bytes(value, 26)

    decoding = DECODING

    return bytes((
        ((decoding[encoded[0]] << 5) | decoding[encoded[1]]) & 0xFF,
        ((decoding[encoded[2]] << 3) | (decoding[encoded[3]] >> 2)) & 0xFF,
        ((decoding[encoded[3]] << 6) | (decoding[encoded[4]] << 1) | (decoding[encoded[5]] >> 4)) & 0xFF,
        ((decoding[encoded[5]] << 4) | (decoding[encoded[6]] >> 1)) & 0xFF,
        ((decoding[encoded[6]] << 7) | (decoding[encoded[7]] << 2) | (decoding[encoded[8]] >> 3)) & 0xFF,
        ((decoding[encoded[8]] << 5) | (decoding[encoded[9]])) & 0xFF,
        ((decoding[encoded[10]] << 3) | (decoding[encoded[11]] >> 2)) & 0xFF,
        ((decoding[encoded[11]] << 6) | (decoding[encoded[12]] << 1) | (decoding[encoded[13]] >> 4)) & 0xFF,
        ((decoding[encoded[13]] << 4) | (decoding[encoded[14]] >> 1)) & 0xFF,
        ((decoding[encoded[14]] << 7) | (decoding[encoded[15]] << 2) | (decoding[encoded[16]] >> 3)) & 0xFF,
        ((decoding[encoded[16]] << 5) | (decoding[encoded[17]])) & 0xFF,
        ((decoding[encoded[18]] << 3) | (decoding[encoded[19]] >> 2)) & 0xFF,
        ((decoding[encoded[19]] << 6) | (decoding[encoded[20]] << 1) | (decoding[encoded[21]] >> 4)) & 0xFF,
        ((decoding[encoded[21]] << 4) | (decoding[encoded[22]] >> 1)) & 0xFF,
        ((decoding[encoded[22]] << 7) | (decoding[encoded[23]] << 2) | (decoding[encoded[24]] >> 3)) & 0xFF,
        ((decoding[encoded[24]] << 5) | (decoding[encoded[25]])) & 0xFF
    ))


def decode_timestamp(timestamp: str) -> bytes:
    """
    Decode the given Base32 encoded :class:`~str` instance to :class:`~bytes`.

    The given :class:`~str` are expected to represent the first 10 characters of a ULID, which
    are the timestamp in milliseconds.

    .. note:: This uses an optimized strategy from the `NUlid` project for decoding ULID
        strings specifically and is not meant for arbitrary decoding.

    :param timestamp: String to decode
    :type timestamp: :class:`~str`
    :return: Value decoded from Base32 string
    :rtype: :class:`~bytes`
    :raises ValueError: when value is not 10 characters
    :raises ValueError: when value cannot be encoded in ASCII
    """
    encoded = str_to_bytes(timestamp, 10)

    decoding = DECODING

    return bytes((
        ((decoding[encoded[0]] << 5) | decoding[encoded[1]]) & 0xFF,
        ((decoding[encoded[2]] << 3) | (decoding[encoded[3]] >> 2)) & 0xFF,
        ((decoding[encoded[3]] << 6) | (decoding[encoded[4]] << 1) | (decoding[encoded[5]] >> 4)) & 0xFF,
        ((decoding[encoded[5]] << 4) | (decoding[encoded[6]] >> 1)) & 0xFF,
        ((decoding[encoded[6]] << 7) | (decoding[encoded[7]] << 2) | (decoding[encoded[8]] >> 3)) & 0xFF,
        ((decoding[encoded[8]] << 5) | (decoding[encoded[9]])) & 0xFF
    ))


def decode_randomness(randomness: str) -> bytes:
    """
    Decode the given Base32 encoded :class:`~str` instance to :class:`~bytes`.

    The given :class:`~str` are expected to represent the last 16 characters of a ULID, which
    are cryptographically secure random values.

    .. note:: This uses an optimized strategy from the `NUlid` project for decoding ULID
        strings specifically and is not meant for arbitrary decoding.

    :param randomness: String to decode
    :type randomness: :class:`~str`
    :return: Value decoded from Base32 string
    :rtype: :class:`~bytes`
    :raises ValueError: when value is not 16 characters
    :raises ValueError: when value cannot be encoded in ASCII
    """
    encoded = str_to_bytes(randomness, 16)

    decoding = DECODING

    return bytes((
        ((decoding[encoded[0]] << 3) | (decoding[encoded[1]] >> 2)) & 0xFF,
        ((decoding[encoded[1]] << 6) | (decoding[encoded[2]] << 1) | (decoding[encoded[3]] >> 4)) & 0xFF,
        ((decoding[encoded[3]] << 4) | (decoding[encoded[4]] >> 1)) & 0xFF,
        ((decoding[encoded[4]] << 7) | (decoding[encoded[5]] << 2) | (decoding[encoded[6]] >> 3)) & 0xFF,
        ((decoding[encoded[6]] << 5) | (decoding[encoded[7]])) & 0xFF,
        ((decoding[encoded[8]] << 3) | (decoding[encoded[9]] >> 2)) & 0xFF,
        ((decoding[encoded[9]] << 6) | (decoding[encoded[10]] << 1) | (decoding[encoded[11]] >> 4)) & 0xFF,
        ((decoding[encoded[11]] << 4) | (decoding[encoded[12]] >> 1)) & 0xFF,
        ((decoding[encoded[12]] << 7) | (decoding[encoded[13]] << 2) | (decoding[encoded[14]] >> 3)) & 0xFF,
        ((decoding[encoded[14]] << 5) | (decoding[encoded[15]])) & 0xFF
    ))


def str_to_bytes(value: str, expected_length: int) -> bytes:
    """
    Convert the given string to bytes and validate it is within the Base32 character set.

    :param value: String to convert to bytes
    :type value: :class:`~str`
    :param expected_length: Expected length of the input string
    :type expected_length: :class:`~int`
    :return: Value converted to bytes.
    :rtype: :class:`~bytes`
    """
    length = len(value)
    if length != expected_length:
        raise ValueError('Expects {} characters for decoding; got {}'.format(expected_length, length))

    try:
        encoded = value.encode('ascii')
    except UnicodeEncodeError as ex:
        raise ValueError('Expects value that can be encoded in ASCII charset: {}'.format(ex)) from ex

    decoding = DECODING

    # Confirm all bytes are valid Base32 decode characters.
    # Note: ASCII encoding handles the out of range checking for us.
    for byte in encoded:
        if decoding[byte] > 31:
            raise ValueError('Non-base32 character found: "{}"'.format(chr(byte)))

    # Confirm most significant bit on timestamp value is limited so it can be stored in 128-bits.
    if length in (10, 26):
        msb = decoding[encoded[0]]
        if msb > 7:
            raise ValueError('Timestamp value too large and will overflow 128-bits. Must be between b"0" and b"7"')

    return encoded
