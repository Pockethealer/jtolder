# backend/models/term.py
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from core.database import Base

class DictionaryTerm(Base):
    __tablename__ = "dictionary_terms"

    id = Column(Integer, primary_key=True, index=True)
    dictionary_id = Column(Integer, ForeignKey("dictionaries.id", ondelete="CASCADE"), nullable=False)
    
    # The exact string in the text (e.g., "㝡", "10日", "〃")
    term = Column(String, nullable=False, index=True) 
    
    # The kana reading (e.g., "とおか", "おなじ"). Can be null for kanji or bilingual dicts.
    reading = Column(String, index=True) 
    
    # For prioritizing which definition shows up first if there are duplicates
    sequence = Column(Integer, default=0) 
    
    # The flexible payload! This holds the rules, meanings, stroke counts, or pitch data.
    definition_data = Column(JSONB, nullable=False) 

    # Composite Index: Yomitan searches often look for BOTH term and reading simultaneously
    __table_args__ = (
        Index('idx_term_reading', 'term', 'reading'),
    )