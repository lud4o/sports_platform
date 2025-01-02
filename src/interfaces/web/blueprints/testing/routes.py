from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from datetime import datetime
from .schemas import (
    TestResultSchema, 
    TestAnalysisSchema,
    BatchUploadSchema,
    TestFilterSchema,
    AnalysisRequestSchema
)
from domain.testing.service.test_management_service import TestManagementService
from domain.testing.service.test_analysis_service import TestAnalysisService

testing_bp = Blueprint('testing', __name__, url_prefix='/api/testing')

def init_testing_routes(test_management_service: TestManagementService, 
                       test_analysis_service: TestAnalysisService):
    
    @testing_bp.route('/tests', methods=['GET'])
    def get_available_tests():
        """Get all available test types"""
        try:
            tests = test_management_service.get_available_test_types()
            return jsonify(tests)
        except Exception as e:
            current_app.logger.error(f"Error getting available tests: {str(e)}")
            return jsonify({"error": "Failed to fetch test types"}), 500

    @testing_bp.route('/tests/<test_id>/results', methods=['POST'])
    def record_test_result():
        """Record a new test result"""
        schema = TestResultSchema()
        try:
            data = schema.load(request.json)
            
            result = test_management_service.record_test_result(
                test_id=data['test_id'],
                athlete_id=data['athlete_id'],
                primary_value=data['primary_value'],
                additional_values=data.get('additional_values'),
                test_date=data.get('test_date', datetime.utcnow())
            )
            
            return jsonify(schema.dump(result)), 201
            
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except Exception as e:
            current_app.logger.error(f"Error recording test result: {str(e)}")
            return jsonify({"error": "Failed to record test result"}), 500

    @testing_bp.route('/athletes/<athlete_id>/tests/<test_id>/progress', methods=['GET'])
    def get_athlete_progress(athlete_id, test_id):
        """Get athlete's progress in a specific test"""
        schema = TestFilterSchema()
        try:
            filters = schema.load(request.args)
            time_period = None
            
            if filters.get('start_date') and filters.get('end_date'):
                time_period = (filters['start_date'], filters['end_date'])
            
            progress = test_analysis_service.get_athlete_progress(
                athlete_id=athlete_id,
                test_id=test_id,
                time_period=time_period
            )
            
            return jsonify(progress)
            
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except Exception as e:
            current_app.logger.error(f"Error getting athlete progress: {str(e)}")
            return jsonify({"error": "Failed to fetch progress"}), 500

    @testing_bp.route('/tests/<test_id>/analysis', methods=['GET'])
    def get_test_analysis(test_id):
        """Get analysis for a specific test result"""
        try:
            result = test_analysis_service.get_analysis(test_id)
            return jsonify(TestAnalysisSchema().dump(result))
        except Exception as e:
            current_app.logger.error(f"Error getting test analysis: {str(e)}")
            return jsonify({"error": "Failed to fetch analysis"}), 500

    @testing_bp.route('/results/batch', methods=['POST'])
    def batch_upload():
        """Handle batch upload of test results"""
        schema = BatchUploadSchema()
        try:
            data = schema.load(request.json)
            
            results = test_management_service.process_batch_upload(
                upload_type=data['type'],
                data=data['data'],
                metadata=data.get('metadata')
            )
            
            return jsonify(results), 201
            
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except Exception as e:
            current_app.logger.error(f"Error processing batch upload: {str(e)}")
            return jsonify({"error": "Failed to process batch upload"}), 500

    @testing_bp.errorhandler(Exception)
    def handle_error(error):
        """Global error handler for testing blueprint"""
        current_app.logger.error(f"Unhandled error in testing blueprint: {str(error)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(error)
        }), 500

    return testing_bp