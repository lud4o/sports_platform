from flask import Blueprint, request, jsonify
from application.test.commands import CreateTestCommand, CreateTestHandler

bp = Blueprint('test_management', __name__)

@bp.route('/tests', methods=['POST'])
def create_test():
    data = request.json
    command = CreateTestCommand(
        name=data['name'],
        category=TestCategory[data['category']],
        primary_unit=TestUnit[data['primary_unit']],
        description=data.get('description'),
        protocol=TestProtocol(**data['protocol']) if 'protocol' in data else None,
        additional_variables=[
            AdditionalVariable(**var) for var in data.get('additional_variables', [])
        ]
    )
    
    handler = CreateTestHandler(test_service)
    test = handler.handle(command)
    
    return jsonify({
        'id': str(test.id),
        'name': test.name,
        'category': test.category.value,
        'primary_unit': test.primary_unit.value
    }), 201

@bp.route('/tests/<uuid:test_id>', methods=['PUT'])
def update_test(test_id):
    data = request.json
    updated_test = test_service.update_test(
        test_id=test_id,
        name=data.get('name'),
        description=data.get('description'),
        protocol=TestProtocol(**data['protocol']) if 'protocol' in data else None,
        additional_variables=[
            AdditionalVariable(**var) for var in data.get('additional_variables', [])
        ]
    )
    
    return jsonify({
        'id': str(updated_test.id),
        'name': updated_test.name,
        'category': updated_test.category.value,
        'primary_unit': updated_test.primary_unit.value
    })