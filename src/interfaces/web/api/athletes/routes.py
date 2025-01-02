from flask import jsonify, request, current_app
from . import athlete_bp
from src.infrastructure.database.models import Athlete
from marshmallow import ValidationError
from .schemas import AthleteSchema
from src.interfaces.web import db

athlete_schema = AthleteSchema()
athletes_schema = AthleteSchema(many=True)

@athlete_bp.route('/', methods=['GET'])
def get_athletes():
    """Get all athletes"""
    athletes = Athlete.query.all()
    return jsonify(athletes_schema.dump(athletes))

@athlete_bp.route('/<uuid:athlete_id>', methods=['GET'])
def get_athlete(athlete_id):
    """Get a specific athlete"""
    athlete = Athlete.query.get_or_404(athlete_id)
    return jsonify(athlete_schema.dump(athlete))

@athlete_bp.route('/', methods=['POST'])
def create_athlete():
    """Create a new athlete"""
    try:
        athlete_data = athlete_schema.load(request.get_json())
        athlete = Athlete(**athlete_data)
        current_app.db.session.add(athlete)
        current_app.db.session.commit()
        return jsonify(athlete_schema.dump(athlete)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

@athlete_bp.route('/<uuid:athlete_id>', methods=['PUT'])
def update_athlete(athlete_id):
    """Update an athlete"""
    athlete = Athlete.query.get_or_404(athlete_id)
    try:
        athlete_data = athlete_schema.load(request.get_json(), partial=True)
        for key, value in athlete_data.items():
            setattr(athlete, key, value)
        current_app.db.session.commit()
        return jsonify(athlete_schema.dump(athlete))
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

@athlete_bp.route('/<uuid:athlete_id>', methods=['DELETE'])
def delete_athlete(athlete_id):
    """Delete an athlete"""
    athlete = Athlete.query.get_or_404(athlete_id)
    current_app.db.session.delete(athlete)
    current_app.db.session.commit()
    return '', 204