#!/usr/bin/env/python
"""Test raise_ise functionality.
"""

import apikit


def test_raise_ise():
    """Test raise_ise functionality.
    """
    try:
        apikit.raise_ise("hippopotamus")
    except apikit.BackendError as exc:
        assert exc.status_code == 500
        assert exc.reason == "Internal Server Error"
        assert exc.content == "hippopotamus"
