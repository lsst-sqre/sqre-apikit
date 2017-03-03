#!/usr/bin/env/python
"""Test retry_request functionality.
"""

import apikit


def test_retry_request():
    """Test retry_request functionality.
    """
    try:
        apikit.retry_request("GET",
                             "http://github.com/lsst-sqre/nonexistent",
                             headers=None, payload=None, auth=None,
                             tries=2, initial_interval=1)
    except apikit.BackendError as exc:
        assert exc.status_code == 500
        assert exc.reason == "Internal Server Error"
