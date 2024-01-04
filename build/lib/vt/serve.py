#!/usr/bin/env python3
"""File watcher system
"""
from flask import Flask, send_from_directory
from .config import __public_dir__, __index_files__
from .vt_logger import logger, print_error
from .render_vanilla_template import render_html
import os

app = Flask(__name__)

port = os.getenv("PORT") or 2220

logger("The serve functionality is not stable yet. Use with caution!", 1)

if not os.path.isdir(__public_dir__):
    print_error(f"VT:WARNING: Static directory '{__public_dir__}' does not exist. Add the directory for your app to serve static content\n")

@app.route('/<path:resource>')
def index(resource):
    if resource.endswith(".html") and resource in __index_files__:
        return render_html(resource)
    return send_from_directory(f"../{__public_dir__}", resource)

@app.route('/')
def default_render():
    return render_html()


def run_flask_app(port: int):
    """ Run flask app
    """
    app.run(debug=True, port=port)

if __name__ == '__main__':
    # Start file watching
    run_flask_app(port)