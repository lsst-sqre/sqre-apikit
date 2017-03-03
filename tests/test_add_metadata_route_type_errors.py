#!/usr/bin/env python
"""Test add_metadata_route function for input parameters causing TypeErrors.
"""
import apikit
import pytest
from flask import Flask

# Yes, it is a very long function name.
# pylint: disable=invalid-name


def test_add_metadata_route_type_errors():
    """Test set_flask_metadata function for parameters causing TypeErrors.
    """
    app = Flask("bob")
    apikit.set_flask_metadata(app, "2.0", "http://example.repo", "BobApp")
    # Add a not-string
    with pytest.raises(TypeError):
        apikit.add_metadata_route(app, 2.0)
    # Add a list with a not-string
    with pytest.raises(TypeError):
        apikit.add_metadata_route(app, [2.0])
