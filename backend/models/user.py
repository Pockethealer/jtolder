# backend/models/user.py
from sqlalchemy import Column, Integer, String
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Target daily reviews (as mentioned in your React Context task)
    daily_review_goal = Column(Integer, default=50)