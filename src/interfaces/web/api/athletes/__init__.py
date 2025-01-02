from flask import Blueprint

athlete_bp = Blueprint('athletes', __name__)

from . import routes  # Import routes after blueprint creation
