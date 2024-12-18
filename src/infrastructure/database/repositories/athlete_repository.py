from typing import List, Optional
from uuid import UUID
from sqlalchemy import or_
from sqlalchemy.orm import Session
from domain.athlete.repository.athlete_repository import AthleteRepository
from domain.athlete.entity.athlete import Athlete
from domain.athlete.entity.value_objects import Name, Gender
from ..models.athlete import AthleteModel

class SQLAlchemyAthleteRepository(AthleteRepository):
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: UUID) -> Optional[Athlete]:
        model = self._session.query(AthleteModel).get(id)
        return model.to_entity() if model else None

    def save(self, athlete: Athlete) -> Athlete:
        model = self._session.query(AthleteModel).get(athlete.id)
        
        if model:
            # Update existing
            model = AthleteModel.from_entity(athlete)
            self._session.merge(model)
        else:
            # Create new
            model = AthleteModel.from_entity(athlete)
            self._session.add(model)
        
        self._session.commit()
        return model.to_entity()

    def find_by_name(self, name: Name) -> Optional[Athlete]:
        model = self._session.query(AthleteModel).filter_by(
            first_name=name.first_name,
            last_name=name.last_name
        ).first()
        return model.to_entity() if model else None

    def find_by_email(self, email: str) -> Optional[Athlete]:
        model = self._session.query(AthleteModel).filter_by(
            email=email
        ).first()
        return model.to_entity() if model else None

    def find_by_criteria(self,
                        age_group: Optional[str] = None,
                        gender: Optional[Gender] = None,
                        sport: Optional[str] = None,
                        custom_team: Optional[str] = None) -> List[Athlete]:
        query = self._session.query(AthleteModel)

        if gender:
            query = query.filter(AthleteModel.gender == gender)
        if sport:
            query = query.filter(AthleteModel.sport == sport)
        if custom_team:
            query = query.filter(AthleteModel.custom_team == custom_team)

        # Age group filtering will be handled after fetching due to dynamic calculation
        athletes = [model.to_entity() for model in query.all()]
        
        if age_group:
            athletes = [athlete for athlete in athletes 
                       if athlete.age_group == age_group or athlete.competitive_age_group == age_group]

        return athletes

    def find_active(self) -> List[Athlete]:
        models = self._session.query(AthleteModel).filter_by(is_active=True).all()
        return [model.to_entity() for model in models]

    def delete(self, id: UUID) -> None:
        model = self._session.query(AthleteModel).get(id)
        if model:
            self._session.delete(model)
            self._session.commit()