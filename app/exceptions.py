# app/exceptions.py
from flask import jsonify

class InvalidUsage(Exception):
    """Custom exception class for invalid usage with HTTP status code."""

    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        """Return dictionary representation of the error message."""
        return {"error": self.message}


def register_error_handlers(app):
    """Register error handlers for the Flask app."""

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        """Handle InvalidUsage exceptions."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def handle_404(_error):
        """Handle 404 Not Found errors."""
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def handle_500(_error):
        """Handle 500 Internal Server errors."""
        return jsonify({"error": "Internal Server Error"}), 500
