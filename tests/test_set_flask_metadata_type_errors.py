#!/usr/bin/env python
"""Test set_flask_metadata function for input parameters causing TypeErrors.
"""
import apikit
import pytest
from flask import Flask


def test_set_flask_metadata():
    """Test set_flask_metadata function for parameters causing TypeErrors.
    """
    # No arguments at all.
    # Obviously the linter is correct here...
    with pytest.raises(TypeError):
        # pylint: disable=no-value-for-parameter
        apikit.set_flask_metadata()
        # First argument is not flask.Flask
    with pytest.raises(TypeError):
        apikit.set_flask_metadata(42, "2.0", "http://example.repo", "BobApp")
    app = Flask("bob")
    # Version is not a string
    with pytest.raises(TypeError):
        apikit.set_flask_metadata(app, 2.0, "http://example.repo", "BobApp")
    # Repository is not a string
    with pytest.raises(TypeError):
        apikit.set_flask_metadata(app, 2.0, ["repo", "man"], "BobApp")
    # Description is not a string
    with pytest.raises(TypeError):
        apikit.set_flask_metadata(app, 2.0, "", "http://example.repo",
                                  {"totally": "bogus"})
    # Auth is not None, the empty string or "none", or a dict
    with pytest.raises(TypeError):
        apikit.set_flask_metadata(
            app, "2.0", "http://example.repo", "BobApp", auth=5)
    # Auth is not None, the empty string or "none", or a dict
    with pytest.raises(TypeError):
        apikit.set_flask_metadata(app, "2.0",
                                  "http://example.repo", "BobApp",
                                  auth="bob")
    # Api_version is not a string
    with pytest.raises(TypeError):
        apikit.set_flask_metadata(app, "2.0", "http://example.repo", "BobApp",
                                  api_version=5, auth="")
