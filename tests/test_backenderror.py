#!/usr/bin/env/python
"""Test BackendError functionality"""

import apikit
import pytest


def test_backenderror():
    """Test BackendError functionality"""
    # Leave out reason
    # Obviously the linter is correct here...
    with pytest.raises(TypeError):
        # pylint: disable=no-value-for-parameter
        apikit.BackendError()
    # Reason not a string
    with pytest.raises(TypeError):
        apikit.BackendError(14)
    # Status code not an integer
    with pytest.raises(TypeError):
        apikit.BackendError("marathon error", 26.2)
    # Content not a basestring
    with pytest.raises(TypeError):
        apikit.BackendError("not a toaster", 922, [])
    # Minimal
    exc = apikit.BackendError("minimal")
    assert exc.reason == "minimal"
    assert exc.status_code == 400
    # Add a status code
    exc = apikit.BackendError("Nae so wee", 789)
    assert exc.status_code == 789
    # Add content
    exc = apikit.BackendError("bad horse", 666, "thoroughbred of sin")
    assert exc.content == "thoroughbred of sin"
    # Check to_dict()
    resultdict = {"reason": exc.reason,
                  "status_code": exc.status_code,
                  "error_content": exc.content}
    assert exc.to_dict() == resultdict
    # Check string representation
    expected = "BackendError: %d %s [%s]" % (exc.status_code, exc.reason,
                                             exc.content)
    assert str(exc) == expected
