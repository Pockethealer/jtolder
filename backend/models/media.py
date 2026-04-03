# backend/models/media.py
from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import Base

class MediaProgress(Base):
    __tablename__ = "media_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # A hash of the local filename/size to identify it across devices
    file_hash = Column(String, nullable=False, index=True) 
    
    # Can hold an EPUB CFI string (e.g., "epubcfi(/6/4[chap01ref]!/4/2/1:0)") 
    # or a Video Timestamp (e.g., "1245.5")
    progress_data = Column(String, nullable=False)