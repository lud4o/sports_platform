from marshmallow import Schema, fields, validate
from datetime import date

class AthleteSchema(Schema):
    """Schema for athlete data validation"""
    id = fields.UUID(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    birthdate = fields.Date(required=True)
    gender = fields.String(required=True, validate=validate.OneOf(['male', 'female']))
    sport = fields.String(required=True)
    email = fields.Email(required=False, allow_none=True)

class TestResultSchema(Schema):
    """Schema for test result data validation"""
    test_id = fields.UUID(required=True)
    athlete_id = fields.UUID(required=True)
    primary_value = fields.Float(required=True)
    additional_values = fields.Dict(keys=fields.String(), values=fields.Float(), required=False)
    test_date = fields.DateTime(required=False)
    conditions = fields.Dict(required=False)

class TestAnalysisSchema(Schema):
    """Schema for test analysis output"""
    metrics = fields.Dict(required=True)
    interpretation = fields.Dict(required=True)
    recommendations = fields.Dict(required=True)
    trend = fields.Dict(required=False)

class GroupSchema(Schema):
    """Schema for group data validation"""
    name = fields.String(required=True)
    type = fields.String(required=True)
    sport = fields.String(required=True)
    gender = fields.String(required=True)
    age_range = fields.Dict(required=False)
    is_custom = fields.Boolean(required=False, default=False)

class BatchUploadSchema(Schema):
    """Schema for batch uploads"""
    type = fields.String(required=True, validate=validate.OneOf(['athletes', 'test_results']))
    data = fields.List(fields.Dict(), required=True)
    metadata = fields.Dict(required=False)

class AnthropometricDataSchema(Schema):
    """Schema for anthropometric data"""
    athlete_id = fields.UUID(required=True)
    date = fields.Date(required=True)
    height = fields.Float(required=False)
    weight = fields.Float(required=False)
    standing_reach = fields.Float(required=False)
    neck_circumference = fields.Float(required=False)
    waist_circumference = fields.Float(required=False)
    hip_circumference = fields.Float(required=False)
    seated_height = fields.Float(required=False)

class TestFilterSchema(Schema):
    """Schema for test result filtering"""
    athlete_id = fields.UUID(required=False)
    group_id = fields.UUID(required=False)
    test_type = fields.String(required=False)
    start_date = fields.DateTime(required=False)
    end_date = fields.DateTime(required=False)
    limit = fields.Integer(required=False, default=10)
    page = fields.Integer(required=False, default=1)

class AnalysisRequestSchema(Schema):
    """Schema for requesting analysis"""
    test_ids = fields.List(fields.UUID(), required=True)
    time_period = fields.Tuple((fields.DateTime(), fields.DateTime()), required=False)
    analysis_type = fields.String(required=True, 
                                validate=validate.OneOf(['single', 'comparative', 'trend']))
    comparison_group = fields.UUID(required=False)  # group_id for comparative analysis