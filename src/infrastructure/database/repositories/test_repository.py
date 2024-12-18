from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from domain.testing.repository.test_repository import TestRepository
from domain.testing.entity.test import Test, TestCategory
from ..models.test import TestModel

class SQLAlchemyTestRepository(TestRepository):
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: UUID) -> Optional[Test]:
        model = self._session.query(TestModel).get(id)
        return model.to_entity() if model else None

    def find_by_name(self, name: str) -> Optional[Test]:
        model = self._session.query(TestModel).filter_by(name=name).first()
        return model.to_entity() if model else None

    def find_by_category(self, category: TestCategory) -> List[Test]:
        models = self._session.query(TestModel).filter_by(category=category).all()
        return [model.to_entity() for model in models]

    def find_with_benchmarks(self, test_id: UUID) -> Optional[Test]:
        model = self._session.query(TestModel)\
            .options(joinedload(TestModel.benchmarks))\
            .get(test_id)
        return model.to_entity() if model else None

    def save(self, test: Test) -> Test:
        model = self._session.query(TestModel).get(test.id)
        if model:
            model = TestModel.from_entity(test)
            self._session.merge(model)
        else:
            model = TestModel.from_entity(test)
            self._session.add(model)
        self._session.commit()
        return model.to_entity()

    def delete(self, id: UUID) -> None:
        model = self._session.query(TestModel).get(id)
        if model:
            self._session.delete(model)
            self._session.commit()