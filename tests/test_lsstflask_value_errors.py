#!/usr/bin/env python
"""Test APIFlask class creation with input parameters causing ValueErrors."""
import apikit
import pytest


def test_lsstflask_value_errors():
    """Test APIFlask class creation with parameters causing ValueErrors."""
    # Empty name
    with pytest.raises(ValueError):
        apikit.APIFlask("", "2.0", "http://example.repo", "BobApp")
    # Empty version
    with pytest.raises(ValueError):
        apikit.APIFlask("bob", "", "http://example.repo", "BobApp")
    # Empty repo
    with pytest.raises(ValueError):
        apikit.APIFlask("bob", "2.0", "", "BobApp")
    # Empty description
    with pytest.raises(ValueError):
        apikit.APIFlask("bob", "2.0", "http://example.repo", "")
    # No field 'type' in 'auth'
    with pytest.raises(ValueError):
        apikit.APIFlask("bob", "2.0",
                        "http://example.repo", "BobApp",
                        auth={"notype": "notbob"})
    # Field 'auth' has 'type' with bad value
    with pytest.raises(ValueError):
        apikit.APIFlask("bob", "2.0",
                        "http://example.repo", "BobApp",
                        auth={"type": "frank",
                              "data": {}})
    # Field 'auth' has correct 'type' but no 'data'
    with pytest.raises(ValueError):
        apikit.APIFlask("bob", "2.0",
                        "http://example.repo", "BobApp",
                        auth={"type": "basic"})
