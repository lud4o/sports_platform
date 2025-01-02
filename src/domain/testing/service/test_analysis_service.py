from typing import Dict, Optional
from uuid import UUID
from datetime import datetime
from ..entity.test import TestResult
from .analysis.speed.sprint_analyzer import SprintAnalyzer
from .analysis.power.jump_profile_analyzer import JumpProfileAnalyzer
from .analysis.strength.imtp_analyzer import IMTPAnalyzer
from infrastructure.database.repositories.test_repository import TestRepository

class TestAnalysisService:
    """Service for managing test analysis through web interface"""
    
    def __init__(self, test_repository: TestRepository):
        self._repository = test_repository
        self._analyzers = {
            "sprint": SprintAnalyzer(test_repository),
            "jump": JumpProfileAnalyzer(test_repository),
            "imtp": IMTPAnalyzer(test_repository)
        }

    def record_and_analyze_test(self,
                              test_name: str,
                              athlete_id: UUID,
                              primary_value: float,
                              additional_values: Optional[Dict] = None,
                              test_date: Optional[datetime] = None) -> Dict:
        """Record test result and perform analysis"""
        # Get test definition
        test_def = self._repository.get_test_by_name(test_name)
        if not test_def:
            raise ValueError(f"Unknown test type: {test_name}")

        # Save test result
        result = self._repository.save_test_result(
            test_definition_id=test_def.id,
            athlete_id=athlete_id,
            primary_value=primary_value,
            additional_values=additional_values,
            test_date=test_date
        )

        # Get appropriate analyzer and analyze
        analyzer = self._get_analyzer(test_def.category)
        if analyzer:
            analysis = analyzer.analyze(athlete_id=athlete_id, test_date=test_date or datetime.utcnow())
            
            # Save analysis results
            self._repository.save_analysis(
                test_result_id=result.id,
                analyzer_type=test_def.category,
                metrics=analysis.get("metrics", {}),
                interpretation=analysis.get("interpretation"),
                recommendations=analysis.get("recommendations")
            )
            
            return {
                "result": result,
                "analysis": analysis
            }

        return {"result": result}

    def _get_analyzer(self, category: str):
        """Get appropriate analyzer for test category"""
        category_mapping = {
            "Speed": "sprint",
            "Power": "jump",
            "Strength": "imtp"
        }
        return self._analyzers.get(category_mapping.get(category.lower()))

    def get_athlete_progress(self,
                           athlete_id: UUID,
                           test_name: str,
                           time_period: Optional[tuple] = None) -> Dict:
        """Get athlete's progress in a specific test"""
        test_def = self._repository.get_test_by_name(test_name)
        if not test_def:
            raise ValueError(f"Unknown test type: {test_name}")

        results = self._repository.get_athlete_results(
            athlete_id=athlete_id,
            test_definition_id=test_def.id,
            start_date=time_period[0] if time_period else None,
            end_date=time_period[1] if time_period else None
        )

        analyzer = self._get_analyzer(test_def.category)
        if analyzer:
            return analyzer.analyze_trend(
                values=[r.primary_value for r in results],
                dates=[r.test_date for r in results]
            )

        return {"results": results}