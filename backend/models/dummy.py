# backend/models/dummy.py
from sqlalchemy import Column, Integer, String
from core.database import Base

class DummyTest(Base):
    __tablename__ = "dummy_test"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)