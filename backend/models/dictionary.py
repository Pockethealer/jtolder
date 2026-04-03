# backend/models/dictionary.py
from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class Dictionary(Base):
    __tablename__ = "dictionaries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False) # e.g., "Jitendex [2023-12-12]" or "JPDB"
    revision = Column(String) # e.g., "3.1" or "kanjidic2"
    is_sequenced = Column(Boolean, default=False) 
    format = Column(Integer) # e.g., 3