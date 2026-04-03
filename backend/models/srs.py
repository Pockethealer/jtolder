# backend/models/srs.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Index
from core.database import Base
from datetime import datetime, timezone

class UserVocab(Base):
    __tablename__ = "user_vocab"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    term = Column(String, nullable=False)
    reading = Column(String, nullable=True) # Optional, in case they save a kanji or phrase
    
    # FSRS Algorithm Data
    state = Column(Integer, default=0) # 0: New, 1: Learning, 2: Review, 3: Relearning
    due = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    stability = Column(Float, default=0.0)
    difficulty = Column(Float, default=0.0)
    reps = Column(Integer, default=0)
    
    # The crucial composite index for the "Batch Tagging" page-load query
    __table_args__ = (
        Index('idx_user_term', 'user_id', 'term'),
    )