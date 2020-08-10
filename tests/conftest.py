"""
    conftest
    ~~~~~~~~

    High level fixtures used across multiple test modules.
"""
import calendar
import datetime
import os
import random

import pytest

from ulid import base32

ASCII_ALPHABET = ''.join(chr(d) for d in range(0, 128))
EXTENDED_ASCII_ALPHABET = ''.join(chr(d) for d in range(128, 256))
ASCII_NON_BASE_32_ALPHABET = ''.join(set(ASCII_ALPHABET).difference(set(base32.ENCODING)))
MSB_ASCII_ALPHABET = ''.join(chr(d) for d in range(48, 56))
MSB_ASCII_INVALID_ALPHABET = ''.join(set(base32.ENCODING).difference(set(MSB_ASCII_ALPHABET)))

MIN_EPOCH = 0
MAX_EPOCH = 281474976710655


@pytest.fixture(scope='session')
def valid_bytes_48_before():
    """
    Fixture that yields a :class:`~bytes` that is 48 bits and is ordered "less than" the
    result of the :func:`~valid_bytes_48_after` fixture.
    """
    return fixed_year_timestamp_bytes(1990, 1, 1)


@pytest.fixture(scope='session')
def valid_bytes_48_after():
    """
    Fixture that yields a :class:`~bytes` that is 48 bits and is ordered "greater than" the
    result of the :func:`~valid_bytes_48_before` fixture.
    """
    return fixed_year_timestamp_bytes(2000, 1, 1)


@pytest.fixture(scope='session')
def valid_bytes_80_before(valid_bytes_48_before):
    """
    Fixture that yields a :class:`~bytes` that is 80 bits and is ordered "less than" the
    result of the :func:`~valid_bytes_80_after` fixture.
    """
    return valid_bytes_48_before + b'\0' * 4


@pytest.fixture(scope='session')
def valid_bytes_80_after(valid_bytes_48_after):
    """
    Fixture that yields a :class:`~bytes` that is 80 bits and is ordered "greater than" the
    result of the :func:`~valid_bytes_80_after` fixture.
    """
    return valid_bytes_48_after + b'\0' * 4


@pytest.fixture(scope='session')
def valid_bytes_128_before(valid_bytes_48_before):
    """
    Fixture that yields a :class:`~bytes` that is 128 bits and is ordered "less than" the
    result of the :func:`~valid_bytes_128_after` fixture.
    """
    return valid_bytes_48_before + b'\0' * 10


@pytest.fixture(scope='session')
def valid_bytes_128_after(valid_bytes_48_after):
    """
    Fixture that yields a :class:`~bytes` that is 128 bits and is ordered "greater than" the
    result of the :func:`~valid_bytes_128_after` fixture.
    """
    return valid_bytes_48_after + b'\0' * 10


@pytest.fixture(scope='function')
def valid_bytes_128():
    """
    Fixture that yields :class:`~bytes` instances that are 128 bits, the length of an entire ULID.
    """
    return random_timestamp_bytes() + random_bytes(10)


@pytest.fixture(scope='function')
def valid_bytes_80():
    """
    Fixture that yields :class:`~bytes` instances that are 80 bits, the length of a ULID randomness.
    """
    return random_bytes(10)


@pytest.fixture(scope='function')
def valid_bytes_48():
    """
    Fixture that yields :class:`~bytes` instances that are 48 bits, the length of a ULID timestamp.
    """
    return random_timestamp_bytes()


@pytest.fixture(scope='function', params=range(16, 32))
def invalid_bytes_128_overflow(request):
    """
    Fixture that yields :class:`~bytes` instances that require more than 128 bits to store.
    """
    return random_non_zero_byte() + random_bytes(request.param, not_in=[16])


@pytest.fixture(scope='function', params=range(0, 32))
def invalid_bytes_128(request):
    """
    Fixture that yields :class:`~bytes` instances that are between 0 and 256 bits, except 128.
    """
    return random_bytes(request.param, not_in=[16])


@pytest.fixture(scope='function', params=range(0, 32))
def invalid_bytes_80(request):
    """
    Fixture that yields :class:`~bytes` instances that are between 0 and 256 bits, except 80.
    """
    return random_bytes(request.param, not_in=[10])


@pytest.fixture(scope='function', params=range(0, 32))
def invalid_bytes_48(request):
    """
    Fixture that yields :class:`~bytes` instances that are between 0 and 256 bits, except 48.
    """
    return random_bytes(request.param, not_in=[6])


@pytest.fixture(scope='function', params=range(0, 32))
def invalid_bytes_48_80_128(request):
    """
    Fixture that yields :class:`~bytes` instances that are between 0 and 256 bits, except 48, 80, and 128.
    """
    return random_bytes(request.param, not_in=[6, 10, 16])


@pytest.fixture(scope='function', params=[10, 16, 26])
def valid_str_valid_length(request):
    """
    Fixture that yields :class:`~str` instances that are 10, 16, and 26 characters.
    """
    return random_str(request.param)


@pytest.fixture(scope='function')
def valid_str_26():
    """
    Fixture that yields :class:`~str` instances that are 26 characters, the length of an entire ULID.
    """
    return random_str(26)


@pytest.fixture(scope='function')
def valid_str_10():
    """
    Fixture that yields :class:`~str` instances that are 10 characters, the length of a ULID timestamp.
    """
    return random_str(10)


@pytest.fixture(scope='function')
def valid_str_16():
    """
    Fixture that yields :class:`~str` instances that are 16 characters, the length of a ULID randomness.
    """
    return random_str(16)


@pytest.fixture(scope='function', params=range(0, 32))
def invalid_str_26(request):
    """
    Fixture that yields :class:`~str` instances that are between 0 and 32 characters, except 26.
    """
    return random_str(request.param, not_in=[26])


@pytest.fixture(scope='function', params=range(0, 32))
def invalid_str_16(request):
    """
    Fixture that yields :class:`~str` instances that are between 0 and 32 characters, except 16.
    """
    return random_str(request.param, not_in=[16])


@pytest.fixture(scope='function', params=range(0, 32))
def invalid_str_10(request):
    """
    Fixture that yields :class:`~str` instances that are between 0 and 32 characters, except 10.
    """
    return random_str(request.param, not_in=[10])


@pytest.fixture(scope='function')
def invalid_str_10_msb_invalid():
    """
    Fixture that yields :class:`~str` instances that are 10 characters long and use an invalid
    MSB.
    """
    return random_str(10, msb_alphabet=MSB_ASCII_INVALID_ALPHABET)


@pytest.fixture(scope='function', params=range(0, 32))
def invalid_str_10_16_26(request):
    """
    Fixture that yields :class:`~str` instances that are between 0 and 32 characters, except 10, 16, and 26.
    """
    return random_str(request.param, not_in=[10, 16, 26])


@pytest.fixture(scope='function', params=range(0, 40))
def invalid_str_10_16_26_32_36(request):
    """
    Fixture that yields :class:`~str` instances that are between 0 and 40 characters, except 10, 16, 26,
    32, and 36.
    """
    return random_str(request.param, not_in=[10, 16, 26, 32, 36])


@pytest.fixture(scope='function', params=[10, 16, 26])
def ascii_non_base32_str_valid_length(request):
    """
    Fixture that yields a :class:`~str` instance that is valid length for a ULID part but contains
    any standard ASCII characters that are not in the Base 32 alphabet.
    """
    return random_str(request.param, alphabet=ASCII_NON_BASE_32_ALPHABET)


@pytest.fixture(scope='function')
def ascii_non_base32_str_26():
    """
    Fixture that yields a :class:`~str` instance that is 26 characters, the length of an entire ULID but
    contains extended ASCII characters.
    """
    return random_str(26, alphabet=ASCII_NON_BASE_32_ALPHABET)


@pytest.fixture(scope='function')
def ascii_non_base32_str_10():
    """
    Fixture that yields a :class:`~str` instance that is 10 characters, the length of a ULID timestamp value but
    contains extended ASCII characters.
    """
    return random_str(10, alphabet=ASCII_NON_BASE_32_ALPHABET)


@pytest.fixture(scope='function')
def ascii_non_base32_str_16():
    """
    Fixture that yields a :class:`~str` instance that is 16 characters, the length of a ULID randomness value but
    contains extended ASCII characters.
    """
    return random_str(16, alphabet=ASCII_NON_BASE_32_ALPHABET)


@pytest.fixture(scope='function', params=[10, 16, 26])
def extended_ascii_str_valid_length(request):
    """
    Fixture that yields a :class:`~str` instance that is valid length for a ULID part but
    contains extended ASCII characters.
    """
    return random_str(request.param, alphabet=EXTENDED_ASCII_ALPHABET)


@pytest.fixture(scope='function')
def extended_ascii_str_26():
    """
    Fixture that yields a :class:`~str` instance that is 26 characters, the length of an entire ULID but
    contains extended ASCII characters.
    """
    return random_str(26, alphabet=EXTENDED_ASCII_ALPHABET)


@pytest.fixture(scope='function')
def extended_ascii_str_10():
    """
    Fixture that yields a :class:`~str` instance that is 10 characters, the length of a ULID timestamp value but
    contains extended ASCII characters.
    """
    return random_str(10, alphabet=EXTENDED_ASCII_ALPHABET)


@pytest.fixture(scope='function')
def extended_ascii_str_16():
    """
    Fixture that yields a :class:`~str` instance that is 16 characters, the length of a ULID randomness value but
    contains extended ASCII characters.
    """
    return random_str(16, alphabet=EXTENDED_ASCII_ALPHABET)


def random_timestamp_bytes():
    """
    Helper function that returns a number of random bytes that represent a timestamp that are within
    the valid range.
    """
    value = random.randint(MIN_EPOCH, MAX_EPOCH - 1)
    return value.to_bytes(6, byteorder='big')


def random_non_zero_byte():
    """
    Helper function that yields a single byte that isn't zero.
    """
    value = random.randint(1, 255)
    return value.to_bytes(1, byteorder='big')


def random_bytes(num_bytes, not_in=(-1,)):
    """
    Helper function that returns a number of random bytes, optionally excluding those of a specific length.
    """
    num_bytes = num_bytes + 1 if num_bytes in not_in else num_bytes
    return os.urandom(num_bytes)


def random_str(num_chars, alphabet=base32.ENCODING, msb_alphabet=MSB_ASCII_ALPHABET, not_in=(-1,)):
    """
    Helper function that returns a string with the specified number of random characters, optionally
    excluding those of a specific length.
    """
    num_chars = num_chars + 1 if num_chars in not_in else num_chars
    return random.choice(msb_alphabet) + ''.join(random.choice(alphabet) for _ in range(num_chars - 1))


def fixed_year_timestamp_bytes(*args, **kwargs):
    """
    Helper function that returns bytes for a :class:`~datetime.datetime` created by the given args.
    """
    timestamp = int(calendar.timegm(datetime.datetime(*args, **kwargs).timetuple())) * 1000
    return timestamp.to_bytes(6, byteorder='big')
