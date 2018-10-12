ulid
====

|Build Status| |Build Status| |codecov| |Code Climate| |Issue Count|

|PyPI Version| |PyPI Versions|

|Updates|

|Documentation Status|

|Stories in Ready|

`Universally Unique Lexicographically Sortable
Identifier <https://github.com/alizain/ulid>`__ in `Python
3 <https://www.python.org/>`__.

Status
~~~~~~

This project is actively maintained.

Installation
~~~~~~~~~~~~

To install ulid from `pip <https://pypi.python.org/pypi/pip>`__:

.. code:: bash

       $ pip install ulid-py

To install ulid from source:

.. code:: bash

       $ git clone git@github.com:ahawker/ulid.git
       $ cd ulid && python setup.py install

Usage
~~~~~

Create a brand new ULID.

The timestamp value (48-bits) is from
`time.time() <https://docs.python.org/3/library/time.html?highlight=time.time#time.time>`__
with millisecond precision.

The randomness value (80-bits) is from
`os.urandom() <https://docs.python.org/3/library/os.html?highlight=os.urandom#os.urandom>`__.

.. code:: python

   >>> import ulid
   >>> ulid.new()
   <ULID('01BJQE4QTHMFP0S5J153XCFSP9')>

Create a new ULID from an existing 128-bit value, such as a
`UUID <https://docs.python.org/3/library/uuid.html>`__.

Supports ULID values as ``int``, ``bytes``, ``str``, and ``UUID`` types.

.. code:: python

   >>> import ulid, uuid
   >>> value = uuid.uuid4()
   >>> value
   UUID('0983d0a2-ff15-4d83-8f37-7dd945b5aa39')
   >>> ulid.from_uuid(value)
   <ULID('09GF8A5ZRN9P1RYDVXV52VBAHS')>

Create a new ULID from an existing timestamp value, such as a
`datetime <https://docs.python.org/3/library/datetime.html#module-datetime>`__
object.

Supports timestamp values as ``int``, ``float``, ``str``, ``bytes``,
``bytearray``, ``memoryview``, ``datetime``, ``Timestamp``, and ``ULID``
types.

.. code:: python

   >>> import datetime, ulid
   >>> ulid.from_timestamp(datetime.datetime(1999, 1, 1))
   <ULID('00TM9HX0008S220A3PWSFVNFEH')>

Create a new ULID from an existing randomness value.

Supports randomness values as ``int``, ``float``, ``str``, ``bytes``,
``bytearray``, ``memoryview``, ``Randomness``, and ``ULID`` types.

.. code:: python

   >>> import os, ulid
   >>> randomness = os.urandom(10)
   >>> ulid.from_randomness(randomness)
   >>> <ULID('01BJQHX2XEDK0VN0GMYWT9JN8S')>

Once you have a ULID object, there are a number of ways to interact with
it.

The ``timestamp`` method will give you a snapshot view of the first
48-bits of the ULID while the ``randomness`` method will give you a
snapshot of the last 80-bits.

.. code:: python

   >>> import ulid
   >>> u = ulid.new()
   >>> u
   <ULID('01BJQM7SC7D5VVTG3J68ABFQ3N')>
   >>> u.timestamp()
   <Timestamp('01BJQM7SC7')>
   >>> u.randomness()
   <Randomness('D5VVTG3J68ABFQ3N')>

The ``ULID``, ``Timestamp``, and ``Randomness`` classes all derive from
the same base class, a ``MemoryView``.

A ``MemoryView`` provides the ``str``, ``int``, and ``bytes`` methods
for changing any values representation.

.. code:: python

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

A ``MemoryView`` also provides rich comparison functionality.

.. code:: python

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

Future Items
~~~~~~~~~~~~

-  Collection of benchmarks to track performance.
-  Backport to Python 2.7?
-  See `Github Issues <https://github.com/ahawker/ulid/issues>`__ for
   more!

Goals
~~~~~

A fast implementation in pure python of the spec with binary format
support.

Contributing
~~~~~~~~~~~~

If you would like to contribute, simply fork the repository, push your
changes and send a pull request. Pull requests will be brought into the
``master`` branch via a rebase and fast-forward merge with the goal of
having a linear branch history with no merge commits.

License
~~~~~~~

`Apache 2.0 <LICENSE>`__

Why not UUID?
-------------

UUID can be suboptimal for many uses-cases because:

-  It isn’t the most character efficient way of encoding 128 bits of
   randomness
-  UUID v1/v2 is impractical in many environments, as it requires access
   to a unique, stable MAC address
-  UUID v3/v5 requires a unique seed and produces randomly distributed
   IDs, which can cause fragmentation in many data structures
-  UUID v4 provides no other information than randomness which can cause
   fragmentation in many data structures

ULID provides:

-  128-bit compatibility with UUID
-  1.21e+24 unique ULIDs per millisecond
-  Lexicographically sortable!
-  Canonically encoded as a 26 character string, as opposed to the 36
   character UUID
-  Uses Crockford’s base32 for better efficiency and readability (5 bits
   per character)
-  Case insensitive
-  No special characters (URL safe)

Specification
-------------

Below is the current specification of ULID as implemented in this
repository.

The binary format is implemented.

::

    01AN4Z07BY      79KA1307SR9X4MV3

   |----------|    |----------------|
    Timestamp          Randomness
     10chars            16chars
      48bits             80bits

Components
~~~~~~~~~~

**Timestamp** \* 48 bit integer \* UNIX-time in milliseconds \* Won’t
run out of space till the year 10895 AD.

**Randomness** \* 80 bits \* Cryptographically secure source of
randomness, if possible

Sorting
~~~~~~~

The left-most character must be sorted first, and the right-most
character sorted last (lexical order). The default ASCII character set
must be used. Within the same millisecond, sort order is not guaranteed

Encoding
~~~~~~~~

Crockford’s Base32 is used as shown. This alphabet excludes the letters
I, L, O, and U to avoid confusion and abuse.

::

   0123456789ABCDEFGHJKMNPQRSTVWXYZ

Binary Layout and Byte Order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The components are encoded as 16 octets. Each component is encoded with
the Most Significant Byte first (network byte order).

::

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

String Representation
~~~~~~~~~~~~~~~~~~~~~

::

   ttttttttttrrrrrrrrrrrrrrrr

   where
   t is Timestamp
   r is Randomness

Links
~~~~~

-  `Original Implementation
   (Javascript) <https://github.com/alizain/ulid>`__
-  `ulid (python) <https://github.com/mdipierro/ulid>`__

.. |Build Status| image:: https://travis-ci.org/ahawker/ulid.svg?branch=master
   :target: https://travis-ci.org/ahawker/ulid
.. |Build Status| image:: https://ci.appveyor.com/api/projects/status/fy0hufnb8h6gwk4d/branch/master?svg=true
   :target: https://ci.appveyor.com/project/ahawker/ulid/branch/master
.. |codecov| image:: https://codecov.io/gh/ahawker/ulid/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ahawker/ulid
.. |Code Climate| image:: https://codeclimate.com/github/ahawker/ulid/badges/gpa.svg
   :target: https://codeclimate.com/github/ahawker/ulid
.. |Issue Count| image:: https://codeclimate.com/github/ahawker/ulid/badges/issue_count.svg
   :target: https://codeclimate.com/github/ahawker/ulid
.. |PyPI Version| image:: https://badge.fury.io/py/ulid-py.svg
   :target: https://badge.fury.io/py/ulid-py
.. |PyPI Versions| image:: https://img.shields.io/pypi/pyversions/ulid-py.svg
   :target: https://pypi.python.org/pypi/ulid-py
.. |Updates| image:: https://pyup.io/repos/github/ahawker/ulid/shield.svg
   :target: https://pyup.io/repos/github/ahawker/ulid/
.. |Documentation Status| image:: https://readthedocs.org/projects/ulid/badge/?version=latest
   :target: http://ulid.readthedocs.io/en/latest/?badge=latest
.. |Stories in Ready| image:: https://badge.waffle.io/ahawker/ulid.svg?label=ready&title=Ready
   :target: http://waffle.io/ahawker/ulid
