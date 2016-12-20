#!/usr/bin/env python
"""Test APIFlask class with legal parameters."""
import apikit


def test_lsstflask():
    """Test APIFlask class with legal parameters."""
    # We need a fresh app each time.
    # Minimal invocation
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp")
    assert flapp.name == "bob"
    assert flapp.config["NAME"] == "bob"
    assert flapp.config["VERSION"] == "2.0"
    assert flapp.config["REPOSITORY"] == "http://example.repo"
    assert flapp.config["API_VERSION"] == "1.0"
    assert flapp.config["DESCRIPTION"] == "BobApp"
    assert isinstance(flapp.config["AUTH"], dict)
    assert flapp.config["AUTH"]["type"] == "none"
    # Invocation with empty string for auth
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                            auth="")
    # Set api_version
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                            api_version="5", auth="")
    assert flapp.config["API_VERSION"] == "5"
    # Auth type string 'none'
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                            auth="none")
    # Auth type 'basic'
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                            auth={"type": "basic",
                                  "data": {}})
    assert flapp.config["AUTH"]["type"] == "basic"
    # Auth type 'bitly-proxy'
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                            auth={"type": "bitly-proxy", "data": {}})
    assert flapp.config["AUTH"]["type"] == "bitly-proxy"
    # Route type string
    # Empty
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                            route="")
    # Specified
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                            route="/bob")
    # Route type list
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                            route=[""])
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                            route=["/bob"])
    # Route type list
    flapp = apikit.APIFlask("bob", "2.0", "http://example.repo", "BobApp",
                            route=["", "/bob"])
