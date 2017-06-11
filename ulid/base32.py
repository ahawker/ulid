"""
    ulid/base32
    ~~~~~~~~~~~

    Functionality for encoding/decoding ULID strings/bytes using Base32 format.

    `Base32 Documentation <http://www.crockford.com/wrmg/base32.html>`
    `NUlid Project <https://github.com/RobThree/NUlid>`
"""
import array


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
     0x0F, 0x10, 0x11, 0xFF, 0x12, 0x13, 0xFF, 0x14, 0x15, 0xFF,
     0x16, 0x17, 0x18, 0x19, 0x1A, 0xFF, 0x1B, 0x1C, 0x1D, 0x1E,
     0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x0A, 0x0B, 0x0C,
     0x0D, 0x0E, 0x0F, 0x10, 0x11, 0xFF, 0x12, 0x13, 0xFF, 0x14,
     0x15, 0xFF, 0x16, 0x17, 0x18, 0x19, 0x1A, 0xFF, 0x1B, 0x1C,
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


def encode_ulid(value: bytes) -> str:
    """
    Encode the given :class:`~bytes` instance to a :class:`~str` using Base32 encoding.

    .. note:: This uses an optimized strategy from the `NUlid` project for encoding ULID
    bytes specifically and is not meant for arbitrary encoding.

    :param value: Bytes to encode
    :type value: :class:`~bytes`
    :return: Value encoded as a Base32 string
    :rtype: :class:`~str`
    :raises ValueError: when the value is not 16 bytes
    """
    if len(value) != 16:
        raise ValueError('Expects 16 bytes for timestamp + randomness; got {}'.format(len(value)))

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
    if len(value) != 26:
        raise ValueError('Expects 26 characters for timestamp + randomness; got {}'.format(len(value)))

    try:
        value = value.encode('ascii')
    except UnicodeEncodeError as ex:
        raise ValueError('Expects value that can be encoded in ASCII charset: {}'.format(ex))

    decoding = DECODING

    return bytes((
        ((decoding[value[0]] << 5) | decoding[value[1]]) & 0xFF,
        ((decoding[value[2]] << 3) | (decoding[value[3]] >> 2)) & 0xFF,
        ((decoding[value[3]] << 6) | (decoding[value[4]] << 1) | (decoding[value[5]] >> 4)) & 0xFF,
        ((decoding[value[5]] << 4) | (decoding[value[6]] >> 1)) & 0xFF,
        ((decoding[value[6]] << 7) | (decoding[value[7]] << 2) | (decoding[value[8]] >> 3)) & 0xFF,
        ((decoding[value[8]] << 5) | (decoding[value[9]])) & 0xFF,
        ((decoding[value[10]] << 3) | (decoding[value[11]] >> 2)) & 0xFF,
        ((decoding[value[11]] << 6) | (decoding[value[12]] << 1) | (decoding[value[13]] >> 4)) & 0xFF,
        ((decoding[value[13]] << 4) | (decoding[value[14]] >> 1)) & 0xFF,
        ((decoding[value[14]] << 7) | (decoding[value[15]] << 2) | (decoding[value[16]] >> 3)) & 0xFF,
        ((decoding[value[16]] << 5) | (decoding[value[17]])) & 0xFF,
        ((decoding[value[18]] << 3) | (decoding[value[19]] >> 2)) & 0xFF,
        ((decoding[value[19]] << 6) | (decoding[value[20]] << 1) | (decoding[value[21]] >> 4)) & 0xFF,
        ((decoding[value[21]] << 4) | (decoding[value[22]] >> 1)) & 0xFF,
        ((decoding[value[22]] << 7) | (decoding[value[23]] << 2) | (decoding[value[24]] >> 3)) & 0xFF,
        ((decoding[value[24]] << 5) | (decoding[value[25]])) & 0xFF
    ))
