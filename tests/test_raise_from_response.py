#!/usr/bin/env/python
"""Test raise_from_response functionality.
"""

import apikit
import requests


def test_raise_ise():
    """Test raise_from_response functionality.
    """
    try:
        resp = requests.get("http://github.com/lsst-sqre/nonexistent")
        apikit.raise_from_response(resp)
    except apikit.BackendError as exc:
        assert exc.status_code == 404
        assert exc.reason == "Not Found"
