from abc import abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.core.repository import Repository
from ..entity.test import Test, TestCategory

class TestRepository(Repository[Test]):
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Test]:
        """Find test by name"""
        pass

    @abstractmethod
    def find_by_category(self, category: TestCategory) -> List[Test]:
        """Find all tests in a category"""
        pass

    @abstractmethod
    def find_with_benchmarks(self, test_id: UUID) -> Optional[Test]:
        """Find test with its benchmarks"""
        pass