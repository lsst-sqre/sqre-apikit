#!/usr/bin/env python
"""Test add_metadata_route function with legal parameters."""
import apikit
from flask import Flask


def test_set_flask_metadata():
    """Test metadata creation with legal parameters."""
    app = Flask("bob")
    apikit.set_flask_metadata(app, "2.0", "http://example.repo", "BobApp")
    apikit.add_metadata_route(app, "")
    apikit.add_metadata_route(app, "bob")
    apikit.add_metadata_route(app, ["bob"])
    apikit.add_metadata_route(app, ["bob", "chuck"])
