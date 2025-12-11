from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from config.database.session import Base

class CommunityORM(Base):
    __tablename__ = "community"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False)
    article_source = Column(String(255), nullable=False)
    content = Column(String(3000), nullable=False)
    tags_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
