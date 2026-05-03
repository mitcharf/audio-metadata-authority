from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class MediaFile(Base):
    __tablename__ = "media_files"
    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True, index=True, nullable=False)
    added = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    hash = Column(String, nullable=True)
    tags = relationship("MediaTag", back_populates="file", cascade="all, delete-orphan", lazy="joined")

class MediaTag(Base):
    __tablename__ = "media_tags"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("media_files.id", ondelete="CASCADE"), index=True, nullable=False)
    tag = Column(String, index=True, nullable=False)
    value = Column(Text, nullable=False)
    file = relationship("MediaFile", back_populates="tags")
