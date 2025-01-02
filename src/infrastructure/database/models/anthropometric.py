from sqlalchemy import Column, Float, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.interfaces.web import db
from sqlalchemy.dialects.postgresql import UUID as pgUUID
import uuid

class AnthropometricData(db.Model):
    __tablename__ = 'anthropometric_data'
    
    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id = Column(pgUUID(as_uuid=True), ForeignKey('athletes.id'), nullable=False)
    date = Column(Date, nullable=False)
    
    height = Column(Float)
    weight = Column(Float)
    standing_reach = Column(Float)
    neck_circumference = Column(Float)
    waist_circumference = Column(Float)
    hip_circumference = Column(Float)
    seated_height = Column(Float)
    
    athlete = db.relationship("Athlete", back_populates="anthropometric_data")
