from typing import Any, Dict, Optional
from flask import jsonify

def success_response(data: Any = None, message: Optional[str] = None, status_code: int = 200):
    """Format successful response"""
    response = {
        'success': True,
        'data': data
    }
    if message:
        response['message'] = message
    return jsonify(response), status_code

def error_response(message: str, error_type: str = 'Error', status_code: int = 400):
    """Format error response"""
    response = {
        'success': False,
        'error': error_type,
        'message': message
    }
    return jsonify(response), status_code