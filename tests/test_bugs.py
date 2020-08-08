"""
    test_bugs
    ~~~~~~~~~

    Tests for validating reported bugs have been fixed.
"""
import copy
import datetime

import pytest

from ulid import api


def test_github_issue_58():
    """
    Assert that :func:`~ulid.api.from_str` can properly decode strings that
    contain Base32 "translate" characters.

    Base32 "translate" characters are: "iI, lL, oO".

    Issue: https://github.com/ahawker/ulid/issues/58
    """
    value = '01BX73KC0TNH409RTFD1JXKmO0'
    instance = api.from_str(value)
    assert instance.str == '01BX73KC0TNH409RTFD1JXKM00'


def test_github_issue_61():
    """
    Assert that :func:`~ulid.api.from_str` will raise a :class:`~ValueError` when given a string
    that contains values not in the Base32 character set.

    In this example, the main character to test is "u" and "U".

    Issue: https://github.com/ahawker/ulid/issues/61
    """
    for s in ('01BX73KC0TNH409RTFD1uXKM00', '01BX73KC0TNH409RTFD1UXKM00'):
        with pytest.raises(ValueError):
            api.from_str(s)


def test_github_issue_452():
    """
    Assert that :class:`~ulid.ulid.ULID` will not raise during a deepcopy.

    Issue: https://github.com/ahawker/ulid/issues/452
    """
    result = copy.deepcopy(api.new())
    assert result is not None


def test_github_issue_463():
    """
    Assert that :meth:`~ulid.ulid.Timestamp.datetime` returns the value as
    a :class:`~datetime.datetime` instance that is UTC aware.

    Issue: https://github.com/ahawker/ulid/issues/463
    """
    instance = api.new()
    assert instance.timestamp().datetime.tzinfo == datetime.timezone.utc
