from flask import Blueprint

test_bp = Blueprint('tests', __name__)

from . import routes