#!/usr/bin/env python
"""Test set_flask_metadata function with legal parameters.
"""
import apikit
from flask import Flask


def test_set_flask_metadata():
    """Test metadata creation with legal parameters.
    """
    # We need a fresh app each time.
    # Minimal invocation
    app = Flask("bob")
    apikit.set_flask_metadata(app, "2.0", "http://example.repo", "BobApp")
    assert app.name == "bob"
    assert app.config["NAME"] == "bob"
    assert app.config["VERSION"] == "2.0"
    assert app.config["REPOSITORY"] == "http://example.repo"
    assert app.config["API_VERSION"] == "1.0"
    assert app.config["DESCRIPTION"] == "BobApp"
    assert isinstance(app.config["AUTH"], dict)
    assert app.config["AUTH"]["type"] == "none"
    # Invocation with empty string for auth
    app = Flask("bob")
    apikit.set_flask_metadata(app, "2.0", "http://example.repo", "BobApp",
                              auth="")
    # Reset name by passing explicit name parameter
    app = Flask("bob")
    apikit.set_flask_metadata(app, "2.0", "http://example.repo", "BobApp",
                              name="tommy")
    assert app.name == "tommy"
    assert app.config["NAME"] == "tommy"
    # Set api_version
    app = Flask("bob")
    apikit.set_flask_metadata(app, "2.0", "http://example.repo", "BobApp",
                              api_version="5", auth="")
    assert app.config["API_VERSION"] == "5"
    # Auth type string 'none'
    app = Flask("bob")
    apikit.set_flask_metadata(app, "2.0", "http://example.repo", "BobApp",
                              auth="none")
    # Auth type 'basic'
    app = Flask("bob")
    apikit.set_flask_metadata(app, "2.0", "http://example.repo", "BobApp",
                              auth={"type": "basic",
                                    "data": {}})
    assert app.config["AUTH"]["type"] == "basic"
    # Auth type 'bitly-proxy'
    app = Flask("bob")
    apikit.set_flask_metadata(app, "2.0", "http://example.repo", "BobApp",
                              auth={"type": "bitly-proxy", "data": {}})
    assert app.config["AUTH"]["type"] == "bitly-proxy"
