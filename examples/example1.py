#!/usr/bin/env python
"""Example with root route and metadata"""
import apikit

# curl http://127.0.0.1:5000/
# curl http://127.0.0.1:5000/metadata


def main():
    """Primary entry point; we supply '/', but the class brings '/metadata'"""
    app = apikit.APIFlask(name="Hello",
                           version="0.0.1",
                           repository="http://example.repo",
                           description="Hello World App")

    # pylint: disable=unused-variable
    @app.route("/")
    def hello_world():
        """The main route."""
        return "Hello, World!"

    app.run()


if __name__ == "__main__":
    main()
