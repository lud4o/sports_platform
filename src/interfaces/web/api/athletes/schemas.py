from marshmallow import Schema, fields, validate
from datetime import date

class AthleteSchema(Schema):
    id = fields.UUID(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    birthdate = fields.Date(required=True)
    gender = fields.String(required=True, validate=validate.OneOf(['male', 'female']))
    sport = fields.String(required=True)
    email = fields.Email(required=False, allow_none=True)
    is_active = fields.Boolean(dump_only=True)