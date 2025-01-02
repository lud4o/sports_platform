from uuid import UUID
from datetime import datetime
from sqlalchemy import Column, String, JSON, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from ....domain.testing.entity.test import Test, TestCategory, TestResult
from ....domain.testing.entity.value_objects import TestUnit, TestProtocol, AdditionalVariable
from .base import BaseModel
from src.interfaces.web import db
import uuid

class TestDefinition(db.Model):
    __tablename__ = 'test_definitions'
    
    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)
    primary_unit = Column(String, nullable=False)
    description = Column(String)
    required_fields = Column(JSON, nullable=False)
    optional_fields = Column(JSON)
    is_active = Column(Boolean, default=True)

    test_results = db.relationship("TestResult", back_populates="test_definition")
    normative_data = db.relationship("NormativeData", back_populates="test_definition")

    def to_entity(self) -> Test:
        """Convert database model to domain entity"""
        additional_vars = []
        if self.optional_fields and 'variables' in self.optional_fields:
            additional_vars = [
                AdditionalVariable(**var) 
                for var in self.optional_fields['variables']
            ]

        protocol = None
        if self.required_fields and 'protocol' in self.required_fields:
            protocol = TestProtocol(**self.required_fields['protocol'])

        return Test(
            id=self.id,
            name=self.name,
            category=TestCategory[self.category.upper()],
            primary_unit=TestUnit[self.primary_unit.upper()],
            description=self.description,
            protocol=protocol,
            additional_variables=additional_vars
        )

    @classmethod
    def from_entity(cls, entity: Test) -> 'TestDefinition':
        """Create database model from domain entity"""
        return cls(
            id=entity.id,
            name=entity.name,
            category=entity.category.value,
            primary_unit=entity.primary_unit.value,
            description=entity.description,
            required_fields={
                'protocol': entity.protocol.__dict__ if entity.protocol else {},
                'unit': entity.primary_unit.value
            },
            optional_fields={
                'variables': [var.__dict__ for var in entity.additional_variables]
            } if entity.additional_variables else {}
        )

class TestResult(db.Model):
    __tablename__ = 'test_results'
    
    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_definition_id = Column(pgUUID(as_uuid=True), ForeignKey('test_definitions.id'), nullable=False)
    athlete_id = Column(pgUUID(as_uuid=True), ForeignKey('athletes.id'), nullable=False)
    test_date = Column(DateTime, nullable=False)
    primary_value = Column(Float, nullable=False)
    additional_values = Column(JSON)
    conditions = Column(JSON)
    validated = Column(Boolean, default=False)

    test_definition = db.relationship("TestDefinition", back_populates="test_results")
    athlete = db.relationship("Athlete", back_populates="test_results")
    analysis_results = db.relationship("TestAnalysis", back_populates="test_result")

    def to_entity(self) -> TestResult:
        """Convert database model to domain entity"""
        return TestResult(
            id=self.id,
            athlete_id=self.athlete_id,
            test_id=self.test_definition_id,
            value=self.primary_value,
            test_date=self.test_date,
            additional_values=self.additional_values or {},
            phase=self.conditions.get('phase') if self.conditions else None
        )

    @classmethod
    def from_entity(cls, entity: TestResult) -> 'TestResult':
        """Create database model from domain entity"""
        return cls(
            id=entity.id,
            test_definition_id=entity.test_id,
            athlete_id=entity.athlete_id,
            test_date=entity.test_date,
            primary_value=entity.value,
            additional_values=entity.additional_values,
            conditions={'phase': entity.phase} if entity.phase else {}
        )

# Keep TestAnalysis and NormativeData classes as they are - they don't need conversion methods
class TestAnalysis(db.Model):
    __tablename__ = 'test_analyses'
    
    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_result_id = Column(pgUUID(as_uuid=True), ForeignKey('test_results.id'), nullable=False)
    analyzer_type = Column(String, nullable=False)
    metrics = Column(JSON, nullable=False)
    interpretation = Column(JSON)
    recommendations = Column(JSON)
    
    test_result = db.relationship("TestResult", back_populates="analysis_results")

class NormativeData(db.Model):
    __tablename__ = 'normative_data'
    
    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_definition_id = Column(pgUUID(as_uuid=True), ForeignKey('test_definitions.id'), nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    percentile = Column(Float)
    
    test_definition = db.relationship("TestDefinition", back_populates="normative_data")