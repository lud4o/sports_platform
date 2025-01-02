from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from domain.testing.repository.test_repository import TestRepository
from domain.testing.entity.test import Test, TestCategory, TestResult
from ..models.test import TestDefinition, TestResult as TestResultModel, TestAnalysis

class SQLAlchemyTestRepository(TestRepository):
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: UUID) -> Optional[Test]:
        """Get test by ID"""
        model = self._session.query(TestDefinition).get(id)
        return model.to_entity() if model else None

    def find_by_name(self, name: str) -> Optional[Test]:
        """Find test by name"""
        model = self._session.query(TestDefinition).filter_by(name=name).first()
        return model.to_entity() if model else None

    def find_by_category(self, category: TestCategory) -> List[Test]:
        """Find all tests in a category"""
        models = self._session.query(TestDefinition).filter_by(category=category).all()
        return [model.to_entity() for model in models]

    def find_with_benchmarks(self, test_id: UUID) -> Optional[Test]:
        """Get test with its benchmarks"""
        model = self._session.query(TestDefinition)\
            .options(joinedload(TestDefinition.normative_data))\
            .get(test_id)
        return model.to_entity() if model else None

    def save(self, test: Test) -> Test:
        """Save or update a test definition"""
        model = self._session.query(TestDefinition).get(test.id)
        if model:
            # Update existing
            model.name = test.name
            model.category = test.category
            model.primary_unit = test.primary_unit
            model.description = test.description
            model.required_fields = test.required_fields
            model.optional_fields = test.optional_fields
        else:
            # Create new
            model = TestDefinition(
                id=test.id,
                name=test.name,
                category=test.category,
                primary_unit=test.primary_unit,
                description=test.description,
                required_fields=test.required_fields,
                optional_fields=test.optional_fields
            )
            self._session.add(model)
        
        self._session.commit()
        return model.to_entity()

    def save_result(self,
                   test_id: UUID,
                   athlete_id: UUID,
                   values: Dict,
                   test_date: Optional[datetime] = None) -> TestResult:
        """Save a test result"""
        result = TestResultModel(
            test_definition_id=test_id,
            athlete_id=athlete_id,
            test_date=test_date or datetime.utcnow(),
            primary_value=values.get('primary_value'),
            additional_values=values
        )
        self._session.add(result)
        self._session.commit()
        return result.to_entity()

    def get_athlete_results(self,
                          athlete_id: UUID,
                          test_id: Optional[UUID] = None,
                          time_period: Optional[tuple] = None,
                          limit: int = 10) -> List[TestResult]:
        """Get athlete's test results"""
        query = self._session.query(TestResultModel)\
            .filter(TestResultModel.athlete_id == athlete_id)
        
        if test_id:
            query = query.filter(TestResultModel.test_definition_id == test_id)
        
        if time_period:
            start_date, end_date = time_period
            if start_date:
                query = query.filter(TestResultModel.test_date >= start_date)
            if end_date:
                query = query.filter(TestResultModel.test_date <= end_date)
        
        results = query.order_by(TestResultModel.test_date.desc())\
            .limit(limit)\
            .all()
            
        return [result.to_entity() for result in results]

    def save_analysis(self,
                     test_result_id: UUID,
                     analysis_data: Dict) -> None:
        """Save analysis results for a test"""
        analysis = TestAnalysis(
            test_result_id=test_result_id,
            analyzer_type=analysis_data.get('analyzer_type'),
            metrics=analysis_data.get('metrics', {}),
            interpretation=analysis_data.get('interpretation'),
            recommendations=analysis_data.get('recommendations')
        )
        self._session.add(analysis)
        self._session.commit()

    def delete(self, id: UUID) -> None:
        """Delete a test definition"""
        model = self._session.query(TestDefinition).get(id)
        if model:
            self._session.delete(model)
            self._session.commit()