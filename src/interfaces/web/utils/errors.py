from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        """Handle HTTP errors"""
        response = {
            'error': error.name,
            'message': error.description
        }
        return jsonify(response), error.code

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        """Handle database errors"""
        response = {
            'error': 'Database Error',
            'message': str(error)
        }
        return jsonify(response), 500

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Handle any other errors"""
        response = {
            'error': 'Internal Server Error',
            'message': str(error)
        }
        return jsonify(response), 500