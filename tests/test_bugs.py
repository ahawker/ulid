"""
    test_bugs
    ~~~~~~~~~

    Tests for validating reported bugs have been fixed.
"""
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
