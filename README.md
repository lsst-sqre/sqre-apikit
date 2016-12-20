[![Build Status](https://travis-ci.org/lsst-sqre/sqre-apikit.svg?branch=master)](https://travis-ci.org/lsst-sqre/sqre-apikit)

# sqre-apikit

LSST DM SQuaRE microservice convenience tools.

## Rationale

In order to create a microservice hosted behind https://api.lsst.codes,
a service will need to provide a route on `/metadata` and
`/v{{api_version}}/metadata`.  That route must serve appropriate
metadata about the service.

### Metadata format

The metadata served must be a JSON object, and must contain the
following fields: 

`name`: `str`

`version`: `str`

`repository`: `str`

`description`: `str`

`api_version`: `str`

`auth`: `str`

The fields `name`, `version`, `api_version`, and `description` are
arbitrary, although semantic versioning is strongly encouraged, and the
API version should reflect the version of the `api.lsst.codes` API in
use (currently `1.0`, documentation pending).

Auth must be one of `none`, `basic`, or `bitly-proxy`.  It represents
the way in which the microservice will authenticate to GitHub: either it
doesn't need to, it uses HTTP Basic Auth with a username and service
token, or it uses the Bitly OAuth2 Proxy with a username, a password,
and the proxy starting-OAuth2 endpoint.

## Provided Functionality

`sqre-apikit` provides one module, `apikit`, which contains three
functions, `set_flask_metadata`, `add_metadata_route`, and
`return_metadata`, and a class, `APIFlask`.

The `set_flask_metadata` sets metadata on an existing Flask app and adds
metadata routes.  `add_metadata_route` is designed to add routing for
each component in the route list to an existing Flask app.
`return_metadata` returns the JSON representation of the metadata for
the service.

The `APIFlask` class creates an instance of a subclass of `flask.Flask`
which has the metadata added and the route(s) already baked into it.

The class comes with a method, `add_route_prefix`, which adds the
metadata route underneath another route.  This is useful, for instance,
if wiring the microservice up through Kubernetes and its Ingress
resources, which provide routing but not rewriting.

## Installation

`sqre-apikit` runs on Python 2.7 or 3.5. You can install it with

```bash
pip install sqre-apikit
```

This will also install the dependency `Flask`.

## Example usage

### `apikit.set_flask_metadata()`

```python
import apikit
import flask

app = flask.Flask("Hello")
apikit.set_flask_metadata(app,
                          version="0.0.1",
                          repository="http://example.repo",
                          description="Hello World App")
```

### `apikit.APIFlask`

```python
import apikit

app = apikit.APIFlask(name="Hello",
                      version="0.0.1",
                      repository="http://example.repo",
                      description="Hello World App")
```

## Development

To develop apikit, create a Python virtual environment, and

```bash
git clone https://github.com/lsst-sqre/sqre-apikit.git
cd sqre-apikit
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python setup.py develop
```
Tests can be run with [pytest](http://pytest.org/latest/):

```bash
py.test tests
```
