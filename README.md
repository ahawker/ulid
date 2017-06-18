# ulid

[![Build Status](https://travis-ci.org/ahawker/ulid.svg?branch=master)](https://travis-ci.org/ahawker/ulid)
[![Test Coverage](https://codeclimate.com/github/ahawker/ulid/badges/coverage.svg)](https://codeclimate.com/github/ahawker/ulid/coverage)
[![Code Climate](https://codeclimate.com/github/ahawker/ulid/badges/gpa.svg)](https://codeclimate.com/github/ahawker/ulid)
[![Issue Count](https://codeclimate.com/github/ahawker/ulid/badges/issue_count.svg)](https://codeclimate.com/github/ahawker/ulid)

[![PyPI Version](https://badge.fury.io/py/ulid-py.svg)](https://badge.fury.io/py/ulid-py)
[![PyPI Versions](https://img.shields.io/pypi/pyversions/ulid-py.svg)](https://pypi.python.org/pypi/ulid-py)
[![PyPI Downloads](https://img.shields.io/pypi/dm/ulid-py.svg)](https://pypi.python.org/pypi/ulid-py)

[![Documentation Status](https://readthedocs.org/projects/ulid/badge/?version=latest)](http://ulid.readthedocs.io/en/latest/?badge=latest)

[Universally Unique Lexicographically Sortable Identifier](https://github.com/alizain/ulid) in [Python 3](https://www.python.org/).

### Status

This project is actively maintained.

### Installation

To install ulid from [pip](https://pypi.python.org/pypi/pip):
```bash
    $ pip install ulid-py
```

To install ulid from source:
```bash
    $ git clone git@github.com:ahawker/ulid.git
    $ cd ulid && python setup.py install
```

### Usage

Create a brand new ULID.

The timestamp value (48-bits) is from [time.time()](https://docs.python.org/3/library/time.html?highlight=time.time#time.time) with millisecond precision.

The randomness value (80-bits) is from [os.urandom()](https://docs.python.org/3/library/os.html?highlight=os.urandom#os.urandom).

```python
>>> import ulid
>>> ulid.new()
<ULID('01BJQE4QTHMFP0S5J153XCFSP9')>
```

Create a new ULID from an existing 128-bit value, such as a [UUID](https://docs.python.org/3/library/uuid.html).

Supports ULID values as `int`, `bytes`, `str`, and `UUID` types.

```python
>>> import ulid, uuid
>>> value = uuid.uuid4()
>>> value
UUID('0983d0a2-ff15-4d83-8f37-7dd945b5aa39')
>>> ulid.from_uuid(value)
<ULID('09GF8A5ZRN9P1RYDVXV52VBAHS')>
```

Create a new ULID from an existing timestamp value, such as a [datetime](https://docs.python.org/3/library/datetime.html#module-datetime) object.

Supports timestamp values as `int`, `float`, `str`, `bytes`, `bytearray`, `memoryview`, and `datetime` types.

```python
>>> import datetime, ulid
>>> ulid.from_timestamp(datetime.datetime(1999, 1, 1))
<ULID('00TM9HX0008S220A3PWSFVNFEH')>
```

Create a new ULID from an existing randomness value.

Supports randomness values as `int`, `float`, `str`, `bytes`, `bytearray`, and `memoryview`.

```python
>>> import os, ulid
>>> randomness = os.urandom(10)
>>> ulid.from_randomness(randomness)
>>> <ULID('01BJQHX2XEDK0VN0GMYWT9JN8S')>
```

Once you have a ULID object, there are a number of ways to interact with it.

The `timestamp` method will give you a snapshot view of the first 48-bits of the ULID while the `randomness` method
will give you a snapshot of the last 80-bits.

```python
>>> import ulid
>>> u = ulid.new()
>>> u
<ULID('01BJQM7SC7D5VVTG3J68ABFQ3N')>
>>> u.timestamp()
<Timestamp('01BJQM7SC7')>
>>> u.randomness()
<Randomness('D5VVTG3J68ABFQ3N')>
```

The `ULID`, `Timestamp`, and `Randomness` classes all derive from the same base class, a `MemoryView`.

A `MemoryView` provides the `str`, `int`, and `bytes` methods for changing any values representation.

```python
>>> import ulid
>>> u = ulid.new()
>>> u
<ULID('01BJQMF54D093DXEAWZ6JYRPAQ')>
>>> u.timestamp()
<Timestamp('01BJQMF54D')>
>>> u.timestamp().int
1497589322893
>>> u.timestamp().bytes
b'\x01\\\xafG\x94\x8d'
>>> u.timestamp().datetime
datetime.datetime(2017, 6, 16, 5, 2, 2, 893000)
>>> u.randomness().bytes
b'\x02F\xde\xb9\\\xf9\xa5\xecYW'
>>> u.bytes[6:] == u.randomness().bytes
True
>>> u.str
'01BJQMF54D093DXEAWZ6JYRPAQ'
>>> u.int
1810474399624548315999517391436142935
```

A `MemoryView` also provides rich comparison functionality.

```python
>>> import datetime, time, ulid
>>> u1 = ulid.new()
>>> time.sleep(5)
>>> u2 = ulid.new()
>>> u1 < u2
True
>>> u3 = ulid.from_timestamp(datetime.datetime(2039, 1, 1))
>>> u1 < u2 < u3
True
>>> [u.timestamp().datetime for u in sorted([u2, u3, u1])]
[datetime.datetime(2017, 6, 16, 5, 7, 14, 847000), datetime.datetime(2017, 6, 16, 5, 7, 26, 775000), datetime.datetime(2039, 1, 1, 8, 0)]
```

### Future Items

* I've been back and fourth on methods vs. properties; finalize!
* Collection of benchmarks to track performance.
* Backport to Python 2.7?
* See [Github Issues](https://github.com/ahawker/ulid/issues) for more!

### Goals

A fast implementation in pure python of the spec with binary format support.

### Contributing

If you would like to contribute, simply fork the repository, push your changes and send a pull request.

### License

[Apache 2.0](LICENSE)

## Specification

Below is the current specification of ULID as implemented in this repository.

The binary format is implemented.

```
 01AN4Z07BY      79KA1307SR9X4MV3

|----------|    |----------------|
 Timestamp          Randomness
  10chars            16chars
   48bits             80bits
```

### Components

**Timestamp**
- 48 bit integer
- UNIX-time in milliseconds
- Won't run out of space till the year 10895 AD.

**Randomness**
- 80 bits
- Cryptographically secure source of randomness, if possible

### Sorting

The left-most character must be sorted first, and the right-most character sorted last (lexical order).
The default ASCII character set must be used. Within the same millisecond, sort order is not guaranteed

### Encoding

Crockford's Base32 is used as shown. This alphabet excludes the letters I, L, O, and U to avoid confusion and abuse.

```
0123456789ABCDEFGHJKMNPQRSTVWXYZ
```

### Binary Layout and Byte Order

The components are encoded as 16 octets. Each component is encoded with the Most Significant Byte first (network byte order).

```
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
```

### String Representation

```
ttttttttttrrrrrrrrrrrrrrrr

where
t is Timestamp
r is Randomness
```
