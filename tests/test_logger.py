#!/usr/bin/env/python
"""Test logger functionality.
"""

import json
import tempfile
import apikit


def test_logger():
    """Test logger functionality.
    """
    testmsg = "Test message"
    tfile = tempfile.NamedTemporaryFile()
    tname = tfile.name
    logger = apikit.get_logger(file=tfile.name)
    logger.warning(testmsg)
    with open(tname) as f:
        wstr = f.read()
    lobj = json.loads(wstr)
    assert lobj["event"] == testmsg
    assert lobj["level"] == "warning"
