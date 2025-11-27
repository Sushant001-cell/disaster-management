"""
Centralized error handlers and logging for the Flask app.

This module exposes `register_error_handlers(app)` which configures
file logging and a global exception handler that logs request info
and stack traces to `../logs/error.log`. In debug mode the traceback
is also returned in the JSON response to aid development.
"""
import os
import logging
import traceback
from logging.handlers import RotatingFileHandler
from flask import jsonify, request
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """Configure logging and register a global exception handler."""
    # Ensure logs directory exists next to project root
    logs_dir = os.path.abspath(os.path.join(app.root_path, '..', 'logs'))
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, 'error.log')
    handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    handler.setLevel(logging.ERROR)

    # Attach handler to Flask app logger
    if not any(isinstance(h, RotatingFileHandler) and getattr(h, 'baseFilename', None) == log_file for h in app.logger.handlers):
        app.logger.addHandler(handler)


    @app.errorhandler(Exception)
    def handle_exception(e):
        # Pass through HTTP exceptions (Flask will handle the response)
        if isinstance(e, HTTPException):
            return e

        # Format traceback and request details
        tb = traceback.format_exc()
        try:
            request_data = None
            if request.is_json:
                request_data = request.get_json(silent=True)
            else:
                request_data = (request.data.decode('utf-8') if request.data else None)
        except Exception:
            request_data = '<unreadable request data>'

        app.logger.error(
            "Unhandled Exception: %s\nPath: %s\nMethod: %s\nRemote: %s\nData: %s\nTraceback:\n%s",
            str(e), request.path, request.method, request.remote_addr, request_data, tb
        )

        # In debug mode, return the traceback to the client for quicker debugging
        if app.debug:
            return jsonify({'error': 'Internal server error', 'exception': str(e), 'traceback': tb}), 500

        return jsonify({'error': 'Internal server error'}), 500
