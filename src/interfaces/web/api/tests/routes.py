from . import test_bp
from src.interfaces.web import db

@test_bp.route('/', methods=['GET'])
def get_tests():
    return {"message": "Tests endpoint"}