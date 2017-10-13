#!/usr/bin/env python
"""Convenience functions for writing LSST microservices"""
import logging
import os
import sys
import time
import logging.handlers
import requests
import structlog
from flask import Flask, jsonify, current_app
# pylint: disable=redefined-builtin,too-many-arguments
from past.builtins import basestring


def set_flask_metadata(app, version, repository, description,
                       api_version="1.0", name=None, auth=None,
                       route=None):
    """
    Sets metadata on the application to be returned via metadata routes.

    Parameters
    ----------
    app : :class:`flask.Flask` instance
        Flask application for the microservice you're adding metadata to.

    version: `str`
        Version of your microservice.

    repository: `str`
        URL of the repository containing your microservice's source code.

    description: `str`
        Description of the microservice.

    api_version: `str`, optional
        Version of the SQuaRE service API framework.  Defaults to '1.0'.

    name : `str`, optional
        Microservice name.  Defaults to the Flask app name.  If set, changes
        the Flask app name to match.

    auth : `dict`, `str`, or `None`
        The 'auth' parameter must be None, the empty string, the string
        'none', or a dict containing a 'type' key, which must be 'none',
        'basic', or 'bitly-proxy'.  If the type is not 'none', there must
        also be a 'data' key containing a dict which holds authentication
        information appropriate to the authentication type.  The legal
        non-dict 'auth' values are equivalent to a 'type' key of 'none'.

    route : `None`, `str`, or list of `str`, optional
        The 'route' parameter must be None, a string, or a list of strings.
        If supplied, each string will be prepended to the metadata route.

    Raises
    ------
    TypeError
        If arguments are not of the appropriate type.
    ValueError
        If arguments are the right type but have illegal values.

    Returns
    -------
        Nothing, but sets `app` metadata and decorates it with `/metadata`
        and `/v{app_version}/metadata` routes.
    """

    errstr = set_flask_metadata.__doc__
    if not isinstance(app, Flask):
        raise TypeError(errstr)
    if name is None:
        name = app.name
    app.config["NAME"] = name
    if app.name != name:
        app.name = name
    app.config["VERSION"] = version
    app.config["REPOSITORY"] = repository
    app.config["DESCRIPTION"] = description
    app.config["API_VERSION"] = api_version
    if not (isinstance(name, str) and isinstance(description, str) and
            isinstance(repository, str) and isinstance(version, str) and
            isinstance(api_version, str)):
        raise TypeError(errstr)
    if not (name and description and repository and version and api_version):
        raise ValueError(errstr)
    if auth is None or (isinstance(auth, str) and ((auth == "none") or
                                                   (auth == ""))):
        auth = {"type": "none",
                "data": None}
    if not isinstance(auth, dict):
        raise TypeError(errstr)
    if "type" not in auth:
        raise ValueError(errstr)
    atp = auth["type"]
    if atp == "none":
        app.config["AUTH"] = {"type": "none",
                              "data": None}
    else:
        if atp not in ["basic", "bitly-proxy"] or "data" not in auth:
            raise ValueError(errstr)
    app.config["AUTH"] = auth
    add_metadata_route(app, route)


def add_metadata_route(app, route):
    """
    Creates a /metadata route that returns service metadata.  Also creates
    a /v{api_version}/metadata route, and those routes with ".json"
    appended.  If route is specified, prepends it (or each component) to the
    front of the route.

    Parameters
    ----------
    app : :class:`flask.Flask` instance
        Flask application for the microservice you're adding metadata to.

    route : `None`, `str`, or list of `str`, optional
        The 'route' parameter must be None, a string, or a list of strings.
        If supplied, each string will be prepended to the metadata route.

    Returns
    -------
        Nothing, but decorates app with `/metadata`
        and `/v{app_version}/metadata` routes.

    """
    errstr = add_metadata_route.__doc__
    if route is None:
        route = [""]
    if isinstance(route, str):
        route = [route]
    if not isinstance(route, list):
        raise TypeError(errstr)
    if not all(isinstance(item, str) for item in route):
        raise TypeError(errstr)
    api_version = app.config["API_VERSION"]

    for rcomp in route:
        # Make canonical
        rcomp = "/" + rcomp.strip("/")
        if rcomp == "/":
            rcomp = ""
        for rbase in ["/metadata", "/v" + api_version + "/metadata"]:
            for rext in ["", ".json"]:
                rte = rcomp + rbase + rext
                with app.app_context():
                    app.add_url_rule(rte, '_return_metadata', _return_metadata)


def _return_metadata():
    """
    Return JSON-formatted metadata for route attachment.
    Requires flask.current_app to be set, which means
     `with app.app_context()`
    """
    app = current_app
    retdict = {"auth": app.config["AUTH"]["type"]}
    for fld in ["name", "repository", "version", "description",
                "api_version"]:
        retdict[fld] = app.config[fld.upper()]
    return jsonify(retdict)


# pylint: disable = too-many-locals, too-many-arguments
def retry_request(method, url, headers=None, payload=None, auth=None,
                  tries=10, initial_interval=5, callback=None):
    """Retry an HTTP request with linear backoff.  Returns the response if
    the status code is < 400 or waits (try * initial_interval) seconds and
    retries (up to tries times) if it
    is not.

    Parameters
    ----------
    method: `str`
        Method: `GET`, `PUT`, or `POST`
    url: `str`
        URL of HTTP request
    headers: `dict`
        HTTP headers to supply.
    payload: `dict`
        Payload for request; passed as parameters to `GET`, JSON message
        body for `PUT`/`POST`.
    auth: `tuple`
        Authentication tuple for Basic/Digest/Custom HTTP Auth.
    tries: `int`
        Number of attempts to make.  Defaults to `10`.
    initial_interval: `int`
        Interval between first and second try, and amount of time added
        before each successive attempt is made.  Defaults to `5`.
    callback : callable
        A callable (function) object that is called each time a retry is
        needed. The callable has a keyword argument signature:

        - ``n``: number of tries completed (integer).
        - ``remaining``: number of tries remaining (integer).
        - ``status``: HTTP status of the previous call.
        - ``content``: body content of the previous call.

    Returns
    -------
    :class:`requests.Response`
        The final HTTP Response received.

    Raises
    ------
    :class:`apikit.BackendError`
        The `status_code` will be `500`, and the reason `Internal Server
        Error`.  Its `content` will be diagnostic of the last response
        received.
    """
    method = method.lower()
    attempt = 1
    while True:
        if method == "get":
            resp = requests.get(url, headers=headers, params=payload,
                                auth=auth)
        elif method == "put" or method == "post":
            resp = requests.put(url, headers=headers, json=payload, auth=auth)
        else:
            raise_ise("Bad method %s: must be 'get', 'put', or 'post" %
                      method)
        if resp.status_code < 400:
            break
        delay = initial_interval * attempt
        if attempt >= tries:
            raise_ise("Failed to '%s' %s after %d attempts." %
                      (method, url, tries) +
                      "  Last response was '%d %s' [%s]" %
                      (resp.status_code, resp.reason, resp.text.strip()))
        if callback is not None:
            callback(n=attempt, remaining=tries - attempt,
                     status=resp.status_code, content=resp.text.strip())
        time.sleep(delay)
        attempt += 1
    return resp


def raise_ise(text):
    """Turn a failed request response into a BackendError that represents
    an Internal Server Error.  Handy for reflecting HTTP errors from farther
    back in the call chain as failures of your service.

    Parameters
    ----------
    text: `str`
        Error text.

    Raises
    ------
    :class:`apikit.BackendError`
        The `status_code` will be `500`, and the reason `Internal Server
        Error`.  Its `content` will be the text you passed.
    """
    if isinstance(text, Exception):
        # Just in case we are exuberantly passed the entire Exception and
        #  not its textual representation.
        text = str(text)
    raise BackendError(status_code=500,
                       reason="Internal Server Error",
                       content=text)


def raise_from_response(resp):
    """Turn a failed request response into a BackendError.  Handy for
    reflecting HTTP errors from farther back in the call chain.

    Parameters
    ----------
    resp: :class:`requests.Response`

    Raises
    ------
    :class:`apikit.BackendError`
        If `resp.status_code` is equal to or greater than 400.
    """
    if resp.status_code < 400:
        # Request was successful.  Or at least, not a failure.
        return
    raise BackendError(status_code=resp.status_code,
                       reason=resp.reason,
                       content=resp.text)


def get_logger(file=None, syslog=False, loghost=None, level=None):
    """Creates a logging object compatible with Python standard logging,
       but which, as a `structlog` instance, emits JSON.

    Parameters
    ----------
    file: `None` or `str` (default `None`)
        If given, send log output to file; otherwise, to `stdout`.
    syslog: `bool` (default `False`)
        If `True`, log to syslog.
    loghost: `None` or `str` (default `None`)
        If given, send syslog output to specified host, UDP port 514.
    level: `None` or `str` (default `None`)
        If given, and if one of (case-insensitive) `DEBUG`, `INFO`,
        `WARNING`, `ERROR`, or `CRITICAL`, log events of that level or
        higher.  Defaults to `WARNING`.


    Returns
    -------
    :class:`structlog.Logger`
        A logging object

    """

    if not syslog:
        if not file:
            handler = logging.StreamHandler(sys.stdout)
        else:
            handler = logging.FileHandler(file)
    else:
        if loghost:
            handler = logging.handlers.SysLogHandler(loghost, 514)
        else:
            handler = logging.handlers.SysLogHandler()
    root_logger = logging.getLogger()
    if level:
        level = level.upper()
        lldict = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        if level in lldict:
            root_logger.setLevel(lldict[level])
    root_logger.addHandler(handler)
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    log = structlog.get_logger()
    return log


class APIFlask(Flask):
    """
    Creates an APIFlask, which is a :class:`flask.Flask` instance subclass
    which already has a /metadata route that serves the correct data, as well
    as a /v{api_version}/metadata route, as well as those routes with ".json"
    appended.

    It is functionally equivalent to calling `apikit.set_flask_metadata` with a
    :class:`Flask.flask` instance as the first argument, except that using
    :class:`apikit.APIFlask` will (obviously) give you an object for which
    `isinstance(obj,apikit.APIFlask)` is true.

    It will also set the Flask config variables `DEBUG` (if the environment
    variable `DEBUG` is set and non-empty, the value will be `True`) and
    `LOGGER`, which will be set to the structlog instance created for this
    object.

    If the environment variable `LOGFILE` is set, the logger will send its
    logs to that file rather than standard output.  If `LOGFILE` is not set and
    `LOG_TO_SYSLOG` is set, the logger will send its logs to syslog, and
    additionally if `LOGHOST` is also set, then the logger will send its logs
    to syslog on LOGHOST port 514 UDP.  If `LOGLEVEL` is set (to one of the
    standard `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`), logs of that
    severity or higher only will be recorded; otherwise the default loglevel
    is `WARNING`.  The environment variable `DEBUG` implies `LOGLEVEL` will be
    treated as `DEBUG`.

    Parameters
    ----------
    name: `str`
        Name of the microservice/Flask application.

    version: `str`
        Version of your microservice.

    repository: `str`
        URL of the repository containing your microservice's source code.

    description: `str`
        Description of the microservice.

    api_version: `str`, optional
        Version of the SQuaRE service API framework.  Defaults to '1.0'.

    auth : `dict`, `str`, or `None`
        The 'auth' parameter must be None, the empty string, the string
        'none', or a dict containing a 'type' key, which must be 'none',
        'basic', or 'bitly-proxy'.  If the type is not 'none', there must
        also be a 'data' key containing a dict which holds authentication
        information appropriate to the authentication type.  The legal
        non-dict 'auth' values are equivalent to a 'type' key of 'none'.

    route : `None`, `str`, or list of `str`, optional
        The 'route' parameter must be None, a string, or a list of strings.
        If supplied, each string will be prepended to the metadata route.

    **kwargs
        Any other arguments to be passed to the :class:`flask.Flask`
        constructor.

    Raises
    ------
    TypeError
        If arguments are not of the appropriate type.

    ValueError
        If arguments are the right type but have illegal values.

    Returns
    -------
        :class:`apikit.APIFlask` instance.

    """

    def __init__(self, name, version, repository, description,
                 api_version="1.0", auth=None, route=None, **kwargs):
        """Initialize a new app"""
        if not isinstance(name, str):
            raise TypeError(APIFlask.__doc__)
        super(APIFlask, self).__init__(name, **kwargs)
        set_flask_metadata(self, description=description,
                           repository=repository,
                           version=version,
                           api_version=api_version,
                           auth=auth,
                           route=route)
        logfile = None
        syslog = False
        loghost = None
        loglevel = None
        if "LOGFILE" in os.environ and os.environ["LOGFILE"]:
            logfile = os.environ["LOGFILE"]
        elif "LOG_TO_SYSLOG" in os.environ and os.environ["LOG_TO_SYSLOG"]:
            syslog = True
            if "LOGHOST" in os.environ and os.environ["LOGHOST"]:
                loghost = os.environ["LOGHOST"]
        if "LOGLEVEL" in os.environ and os.environ["LOGLEVEL"]:
            loglevel = os.environ["LOGLEVEL"]
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            self.debug = True
            self.config["DEBUG"] = True
            loglevel = "DEBUG"
        log = get_logger(file=logfile, syslog=syslog, loghost=loghost,
                         level=loglevel)
        self.config["LOGGER"] = log

    def add_route_prefix(self, route):
        """Add a new route at the front of the metadata routes."""
        add_metadata_route(self, route)


class BackendError(Exception):
    """
    Creates a JSON-formatted error for use in LSST/DM microservices.

    Parameters
    ----------
    reason: `str`
        Reason for the exception

    status_code: `int`, optional
        Status code to be returned, defaults to 400.

    content: `str`, optional
        Textual content of the underlying error.

    Returns
    -------
    :class:`apikit.BackendError` instance.  This class will have the
    following fields:

    `reason`: `str` or `None`

    `status_code`: `int`

    `content`: `basestr` (Python3: `past.builtins.basestring`) or `None`

    Notes
    -----
    This class is intended for use pretty much as described at
    (http://flask.pocoo.org/docs/0.11/patterns/apierrors/).
    """

    reason = None
    status_code = 400
    content = None

    def __init__(self, reason, status_code=None, content=None):
        """Exception for target service error."""
        Exception.__init__(self)
        if not isinstance(reason, str):
            raise TypeError("'reason' must be a str")
        self.reason = reason
        if status_code is not None:
            if isinstance(status_code, int):
                self.status_code = status_code
            else:
                raise TypeError("'status_code' must be an int")
        if content is not None:
            if not isinstance(content, basestring):
                raise TypeError("'content' must be a basestring")
        self.content = content

    def __str__(self):
        """Useful textual representation"""
        return "BackendError: %d %s [%s]" % (self.status_code,
                                             self.reason, self.content)

    def to_dict(self):
        """Convenience method for creating custom error pages.
        Returns
        -------

        `dict` : A dictionary with the following fields:

            `reason`: `str` or `None`
            `status_code`: `str`
            `error_content`: `str` or `None`

            The intention is to pass the resulting dict to `flask.jsonify()`
            to create a custom error response.
        """
        return {"reason": self.reason,
                "status_code": self.status_code,
                "error_content": self.content}
