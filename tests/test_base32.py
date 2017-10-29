"""
    test_base32
    ~~~~~~~~~~~

    Tests for the :mod:`~ulid.base32` module.
"""
import pytest

from ulid import base32


NON_BASE_32_EXC_REGEX = r'^Non-base32 character found'
ENCODE_BYTE_SIZE_EXC_REGEX = r'^Expects bytes in sizes of'
ENCODE_ULID_BYTE_SIZE_EXC_REGEX = r'Expects 16 bytes for'


@pytest.fixture(scope='session')
def decoding_alphabet():
    """
    Fixture that yields the entire alphabet that is valid for base32 decoding.
    """
    return base32.ENCODING + 'lLiIoO'


def test_encode_handles_ulid_and_returns_26_char_string(valid_bytes_128):
    """
    Assert that :func:`~ulid.base32.encode` encodes a valid 128 bit bytes object into a :class:`~str`
    that is 26 characters long.
    """
    encoded = base32.encode(valid_bytes_128)
    assert isinstance(encoded, str)
    assert len(encoded) == 26


def test_encode_handles_timestamp_and_returns_10_char_string(valid_bytes_48):
    """
    Assert that :func:`~ulid.base32.encode` encodes a valid 48 bit bytes object into a :class:`~str`
    that is 10 characters long.
    """
    encoded = base32.encode(valid_bytes_48)
    assert isinstance(encoded, str)
    assert len(encoded) == 10


def test_encode_handles_randomness_and_returns_16_char_string(valid_bytes_80):
    """
    Assert that :func:`~ulid.base32.encode` encodes a valid 80 bit bytes object into a :class:`~str`
    that is 16 characters long.
    """
    encoded = base32.encode(valid_bytes_80)
    assert isinstance(encoded, str)
    assert len(encoded) == 16


def test_encode_raises_on_bytes_length_mismatch(invalid_bytes_48_80_128):
    """
    Assert that :func:`~ulid.base32.encode` raises a :class:`~ValueError` when given a :class:`~bytes`
    instance that is not exactly 48, 80, or 128 bits in length.
    """
    with pytest.raises(ValueError) as ex:
        base32.encode(invalid_bytes_48_80_128)
    assert ex.match(ENCODE_BYTE_SIZE_EXC_REGEX)


def test_encode_ulid_returns_26_char_string(valid_bytes_128):
    """
    Assert that :func:`~ulid.base32.encode_ulid` encodes a valid 128 bit bytes object into a :class:`~str`
    that is 26 characters long.
    """
    encoded = base32.encode_ulid(valid_bytes_128)
    assert isinstance(encoded, str)
    assert len(encoded) == 26


def test_encode_ulid_raises_on_bytes_length_mismatch(invalid_bytes_128):
    """
    Assert that :func:`~ulid.base32.encode_ulid` raises a :class:`~ValueError` when given a :class:`~bytes`
    instance that is not exactly 128 bit.
    """
    with pytest.raises(ValueError) as ex:
        base32.encode_ulid(invalid_bytes_128)
    assert ex.match(ENCODE_ULID_BYTE_SIZE_EXC_REGEX)


def test_encode_timestamp_returns_10_char_string(valid_bytes_48):
    """
    Assert that :func:`~ulid.base32.encode_timestamp` encodes a valid 48 bit bytes object into a :class:`~str`
    that is 10 characters long.
    """
    encoded = base32.encode_timestamp(valid_bytes_48)
    assert isinstance(encoded, str)
    assert len(encoded) == 10


def test_encode_timestamp_raises_on_bytes_length_mismatch(invalid_bytes_48):
    """
    Assert that :func:`~ulid.base32.encode_timestamp` raises a :class:`~ValueError` when given a :class:`~bytes`
    instance that is not exactly 48 bit.
    """
    with pytest.raises(ValueError):
        base32.encode_timestamp(invalid_bytes_48)


def test_encode_randomness_returns_16_char_string(valid_bytes_80):
    """
    Assert that :func:`~ulid.base32.encode_randomness` encodes a valid 80 bit bytes object into a :class:`~str`
    that is 16 characters long.
    """
    encoded = base32.encode_randomness(valid_bytes_80)
    assert isinstance(encoded, str)
    assert len(encoded) == 16


def test_encode_randomness_raises_on_bytes_length_mismatch(invalid_bytes_80):
    """
    Assert that :func:`~ulid.base32.encode_randomness` raises a :class:`~ValueError` when given a :class:`~bytes`
    instance that is not exactly 80 bit.
    """
    with pytest.raises(ValueError):
        base32.encode_randomness(invalid_bytes_80)


def test_decode_handles_ulid_and_returns_16_bytes(valid_str_26):
    """
    Assert that :func:`~ulid.base32.decode` decodes a valid 26 character string into a :class:`~bytes`
    instance that is 128 bit.
    """
    decoded = base32.decode(valid_str_26)
    assert isinstance(decoded, bytes)
    assert len(decoded) == 16


def test_decode_handles_timestamp_and_returns_6_bytes(valid_str_10):
    """
    Assert that :func:`~ulid.base32.decode` decodes a valid 10 character string into a :class:`~bytes`
    instance that is 48 bit.
    """
    decoded = base32.decode(valid_str_10)
    assert isinstance(decoded, bytes)
    assert len(decoded) == 6


def test_decode_handles_randomness_and_returns_10_bytes(valid_str_16):
    """
    Assert that :func:`~ulid.base32.decode` decodes a valid 16 character string into a :class:`~bytes`
    instance that is 80 bit.
    """
    decoded = base32.decode(valid_str_16)
    assert isinstance(decoded, bytes)
    assert len(decoded) == 10


def test_decode_raises_on_str_length_mismatch(invalid_str_10_16_26):
    """
    Assert that :func:`~ulid.base32.decode` raises a :class:`~ValueError` when given a :class:`~str`
    instance that is not exactly 10, 16, 26 characters in length.
    """
    with pytest.raises(ValueError):
        base32.decode(invalid_str_10_16_26)


def test_decode_raises_on_extended_ascii_str(extended_ascii_str_valid_length):
    """
    Assert that :func:`~ulid.base32.decode` raises a :class:`~ValueError` when given a :class:`~str`
    instance that contains extended ascii characters.
    """
    with pytest.raises(ValueError):
        base32.decode(extended_ascii_str_valid_length)


def test_decode_raises_on_non_base32_decode_char(ascii_non_base32_str_valid_length):
    """
    Assert that :func:`~ulid.base32.decode_ulid` raises a :class:`~ValueError` when given a :class:`~str`
    instance that includes ASCII characters not part of the Base 32 decoding character set.
    """
    with pytest.raises(ValueError) as ex:
        base32.decode(ascii_non_base32_str_valid_length)
    ex.match(NON_BASE_32_EXC_REGEX)


def test_decode_ulid_returns_16_bytes(valid_str_26):
    """
    Assert that :func:`~ulid.base32.decode_ulid` decodes a valid 26 character string into a :class:`~bytes`
    instance that is 128 bit.
    """
    decoded = base32.decode_ulid(valid_str_26)
    assert isinstance(decoded, bytes)
    assert len(decoded) == 16


def test_decode_ulid_raises_on_str_length_mismatch(invalid_str_26):
    """
    Assert that :func:`~ulid.base32.decode_ulid` raises a :class:`~ValueError` when given a :class:`~str`
    instance that is not exactly 26 chars.
    """
    with pytest.raises(ValueError):
        base32.decode_ulid(invalid_str_26)


def test_decode_ulid_raises_on_non_ascii_str(extended_ascii_str_26):
    """
    Assert that :func:`~ulid.base32.decode_ulid` raises a :class:`~ValueError` when given a :class:`~str`
    instance that contains extended ascii characters.
    """
    with pytest.raises(ValueError):
        base32.decode_ulid(extended_ascii_str_26)


def test_decode_ulid_raises_on_non_base32_decode_char(ascii_non_base32_str_26):
    """
    Assert that :func:`~ulid.base32.decode_ulid` raises a :class:`~ValueError` when given a :class:`~str`
    instance that includes ASCII characters not part of the Base 32 decoding character set.
    """
    with pytest.raises(ValueError) as ex:
        base32.decode_ulid(ascii_non_base32_str_26)
    ex.match(NON_BASE_32_EXC_REGEX)


def test_decode_timestamp_returns_6_bytes(valid_str_10):
    """
    Assert that :func:`~ulid.base32.decode_timestamp` decodes a valid 10 character string into a :class:`~bytes`
    instance that is 48 bit.
    """
    decoded = base32.decode_timestamp(valid_str_10)
    assert isinstance(decoded, bytes)
    assert len(decoded) == 6


def test_decode_timestamp_raises_on_str_length_mismatch(invalid_str_10):
    """
    Assert that :func:`~ulid.base32.decode_timestamp` raises a :class:`~ValueError` when given a :class:`~str`
    instance that is not exactly 10 chars.
    """
    with pytest.raises(ValueError):
        base32.decode_timestamp(invalid_str_10)


def test_decode_timestamp_raises_on_non_ascii_str(extended_ascii_str_10):
    """
    Assert that :func:`~ulid.base32.decode_timestamp` raises a :class:`~ValueError` when given a :class:`~str`
    instance that contains extended ascii characters.
    """
    with pytest.raises(ValueError):
        base32.decode_timestamp(extended_ascii_str_10)


def test_decode_timestamp_raises_on_non_base32_decode_char(ascii_non_base32_str_10):
    """
    Assert that :func:`~ulid.base32.decode_timestamp` raises a :class:`~ValueError` when given a :class:`~str`
    instance that includes ASCII characters not part of the Base 32 decoding character set.
    """
    with pytest.raises(ValueError) as ex:
        base32.decode_timestamp(ascii_non_base32_str_10)
    ex.match(NON_BASE_32_EXC_REGEX)


def test_decode_randomness_returns_10_bytes(valid_str_16):
    """
    Assert that :func:`~ulid.base32.decode_randomness` decodes a valid 16 character string into a :class:`~bytes`
    instance that is 80 bit.
    """
    decoded = base32.decode_randomness(valid_str_16)
    assert isinstance(decoded, bytes)
    assert len(decoded) == 10


def test_decode_randomness_raises_on_str_length_mismatch(invalid_str_16):
    """
    Assert that :func:`~ulid.base32.decode_randomness` raises a :class:`~ValueError` when given a :class:`~str`
    instance that is not exactly 16 chars.
    """
    with pytest.raises(ValueError):
        base32.decode_randomness(invalid_str_16)


def test_decode_randomness_raises_on_non_ascii_str(extended_ascii_str_16):
    """
    Assert that :func:`~ulid.base32.decode_randomness` raises a :class:`~ValueError` when given a :class:`~str`
    instance that contains extended ascii characters.
    """
    with pytest.raises(ValueError):
        base32.decode_randomness(extended_ascii_str_16)


def test_decode_randomness_raises_on_non_base32_decode_char(ascii_non_base32_str_16):
    """
    Assert that :func:`~ulid.base32.decode_randomness` raises a :class:`~ValueError` when given a :class:`~str`
    instance that includes ASCII characters not part of the Base 32 decoding character set.
    """
    with pytest.raises(ValueError) as ex:
        base32.decode_randomness(ascii_non_base32_str_16)
    ex.match(NON_BASE_32_EXC_REGEX)


def test_decode_table_has_value_for_entire_decoding_alphabet(decoding_alphabet):
    """
    Assert that :attr:`~ulid.base32.DECODING` stores a valid value mapping for all characters that
    can be base32 decoded.
    """
    for char in decoding_alphabet:
        assert base32.DECODING[ord(char)] != 0xFF, 'Character "{}" decoded improperly'.format(char)


def test_str_to_bytes_returns_expected_bytes(valid_str_valid_length):
    """
    Assert that :func:`~ulid.base32.str_to_bytes` decodes a valid string that is 10, 16, or 26 characters long
    into a :class:`~bytes` instance.
    """
    decoded = base32.str_to_bytes(valid_str_valid_length, len(valid_str_valid_length))
    assert isinstance(decoded, bytes)
    assert len(decoded) == len(valid_str_valid_length)


def test_str_to_bytes_raises_on_unexpected_length(invalid_str_26):
    """
    Assert that :func:`~ulid.base32.str_to_bytes` raises a :class:`~ValueError` when given a :class:`~str`
    instance that does not match the expected length.
    """
    with pytest.raises(ValueError):
        base32.str_to_bytes(invalid_str_26, 26)


def test_str_to_bytes_raises_on_extended_ascii_str(extended_ascii_str_valid_length):
    """
    Assert that :func:`~ulid.base32.str_to_bytes` raises a :class:`~ValueError` when given a :class:`~str`
    instance that includes extended ascii characters.
    """
    with pytest.raises(ValueError):
        base32.str_to_bytes(extended_ascii_str_valid_length, len(extended_ascii_str_valid_length))


def test_str_to_bytes_raises_on_non_base32_decode_char(ascii_non_base32_str_valid_length):
    """
    Assert that :func:`~ulid.base32.str_to_bytes` raises a :class:`~ValueError` when given a :class:`~str`
    instance that includes ASCII characters not part of the Base 32 decoding character set.
    """
    with pytest.raises(ValueError) as ex:
        base32.str_to_bytes(ascii_non_base32_str_valid_length, len(ascii_non_base32_str_valid_length))
    ex.match(NON_BASE_32_EXC_REGEX)
