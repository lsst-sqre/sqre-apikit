#!/usr/bin/env python
"""Test set_flask_metadata function for input parameters causing ValueErrors."""
import apikit
import pytest
from flask import Flask

# Yes, it is a very long fimctopm name.
# pylint: disable=invalid-name


def test_set_flask_metadata_value_errors():
    """Test set_flask_metadata for input parameters causing ValueErrors."""
    app = Flask("bob")
    # Empty version
    with pytest.raises(ValueError):
        apikit.set_flask_metadata(app, "", "http://example.repo", "BobApp")
        # Empty repo
    with pytest.raises(ValueError):
        apikit.set_flask_metadata(app, "2.0", "", "BobApp")
    # Empty description
    with pytest.raises(ValueError):
        apikit.set_flask_metadata(app, "2.0", "http://example.repo", "")
    # No field 'type' in 'auth'
    with pytest.raises(ValueError):
        apikit.set_flask_metadata(app, "2.0",
                                  "http://example.repo", "BobApp",
                                  auth={"notype": "notbob"})
    # Field 'auth' has 'type' with bad value
    with pytest.raises(ValueError):
        apikit.set_flask_metadata(app, "2.0",
                                  "http://example.repo", "BobApp",
                                  auth={"type": "frank",
                                        "data": {}})
    # Field 'auth' has correct 'type' but no 'data'
    with pytest.raises(ValueError):
        apikit.set_flask_metadata(app, "2.0",
                                  "http://example.repo", "BobApp",
                                  auth={"type": "basic"})
