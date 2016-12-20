#!/usr/bin/env python
"""Test APIFlask class for input parameters causing TypeErrors."""
import apikit
import pytest


def test_lsstflask_type_errors():
    """Test APIFlask for input parameters causing TypeErrors."""
    # No arguments at all.
    # Obviously the linter is correct here...
    with pytest.raises(TypeError):
        # pylint: disable=no-value-for-parameter
        apikit.APIFlask()
    # Name is not a string
    with pytest.raises(TypeError):
        apikit.APIFlask(("Beer", "me"), "2.0", "http://example.repo",
                        "BobApp")
    # Version is not a string
    with pytest.raises(TypeError):
        apikit.APIFlask("bob", 2.0, "http://example.repo", "BobApp")
    # Repository is not a string
    with pytest.raises(TypeError):
        apikit.APIFlask("bob", 2.0, ["repo", "man"], "BobApp")
    # Description is not a string
    with pytest.raises(TypeError):
        apikit.APIFlask("bob", 2.0, "", "http://example.repo",
                        {"totally": "bogus"})
    # Auth is not None, the empty string or "none", or a dict
    with pytest.raises(TypeError):
        apikit.APIFlask("bob", "2.0", "http://example.repo",
                        "BobApp", auth=5)
    # Auth is not None, the empty string or "none", or a dict
    with pytest.raises(TypeError):
        apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                        auth="bob")
    # Api_version is not a string
    with pytest.raises(TypeError):
        apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                        api_version=5, auth="")
    # Route is not None, a string, or a list of strings
    with pytest.raises(TypeError):
        apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                        route=2)
    # Route is a list that contains a non-string
    with pytest.raises(TypeError):
        apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                        route=[2])
