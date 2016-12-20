#!/usr/bin/env python
"""Convenience functions for writing LSST microservices"""
from flask import Flask, jsonify, current_app
from past.builtins import basestring
# pylint: disable=too-many-arguments


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
    name = app.config["NAME"]
    api_version = app.config["API_VERSION"]
    repository = app.config["REPOSITORY"]
    version = app.config["VERSION"]
    description = app.config["DESCRIPTION"]
    auth = app.config["AUTH"]["type"]

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
