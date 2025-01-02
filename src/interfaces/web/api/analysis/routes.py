from . import analysis_bp
from src.interfaces.web import db

@analysis_bp.route('/', methods=['GET'])
def get_analysys():
    return {"message": "Analysis endpoint"}