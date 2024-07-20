from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from core.libs import helpers
from core.libs.exceptions import FyleError

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    @app.route('/')
    def ready():
        """Health check endpoint"""
        response = jsonify({
            'status': 'ready',
            'time': helpers.get_utc_now()
        })
        return response

    @app.errorhandler(Exception)
    def handle_error(err):
        """Global error handler"""
        if isinstance(err, FyleError):
            return jsonify(
                error='FyleError', message=err.message
            ), err.status_code
        elif isinstance(err, ValidationError):
            return jsonify(
                error='ValidationError', message=err.messages
            ), 400
        elif isinstance(err, IntegrityError):
            return jsonify(
                error='IntegrityError', message=str(err.orig)
            ), 400
        elif isinstance(err, HTTPException):
            return jsonify(
                error=err.__class__.__name__, message=str(err)
            ), err.code

        # For other exceptions, return a generic 500 error
        return jsonify(
            error='InternalServerError', message='An unexpected error occurred'
        ), 500

    return app

if __name__ == '__main__':
    # Create an app instance and run the server
    app = create_app()
    app.run(debug=False)  # Ensure debug=True is not used in production
