from sqlalchemy import Column, String, JSON, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BaseModel

class BatchOperation(BaseModel):
    """Tracks batch operations like bulk uploads"""
    __tablename__ = 'batch_operations'
    
    type = Column(String, nullable=False)  # 'test_results', 'athletes', etc.
    status = Column(String, nullable=False)  # 'pending', 'processing', 'completed', 'failed'
    total_items = Column(Integer, nullable=False)
    processed_items = Column(Integer, default=0)
    errors = Column(JSON)  # Store any error messages
    batch_metadata = Column(JSON)  # Changed from metadata to batch_metadata
    completed_at = Column(DateTime)

    results = relationship("BatchResult", back_populates="batch_operation")

class BatchResult(BaseModel):
    """Individual results from batch operations"""
    __tablename__ = 'batch_results'
    
    batch_operation_id = Column(UUID(as_uuid=True), ForeignKey('batch_operations.id'), nullable=False)
    item_index = Column(Integer, nullable=False)  # Position in original batch
    status = Column(String, nullable=False)  # 'success', 'failed'
    error_message = Column(String)
    result_id = Column(UUID(as_uuid=True))  # ID of created/updated record
    
    batch_operation = relationship("BatchOperation", back_populates="results")