from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from config.database.session import Base


class TagsORM(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    tags_value = Column(String(255), nullable=False)
    tags_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)