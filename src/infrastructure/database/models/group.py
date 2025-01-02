from uuid import UUID
from sqlalchemy import Column, String, JSON, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship
from .base import BaseModel
from src.interfaces.web import db
import uuid
from sqlalchemy.dialects.postgresql import UUID as pgUUID

class Group(db.Model):
    __tablename__ = 'groups'
    
    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'natural', 'custom'
    sport = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age_range = Column(JSON)  # {"min": 14, "max": 16} for age groups
    is_custom = Column(Boolean, default=False)
    group_metadata = Column(JSON)  # Changed from metadata to group_metadata

    athletes = relationship("Athlete", 
                          secondary="athlete_groups",
                          back_populates="groups")

    __table_args__ = (
        UniqueConstraint('sport', 'gender', 'name', name='unq_group_sport_gender_name'),
    )

class AthleteGroup(db.Model):
    __tablename__ = 'athlete_groups'

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id = Column(pgUUID(as_uuid=True), ForeignKey('athletes.id', ondelete='CASCADE'), nullable=False)
    group_id = Column(pgUUID(as_uuid=True), ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    is_primary = Column(Boolean, default=True)
    
    __table_args__ = (
        UniqueConstraint('athlete_id', 'group_id', name='unq_athlete_group'),
    )