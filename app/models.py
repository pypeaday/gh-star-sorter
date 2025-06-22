from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, unique=True, index=True)
    name = Column(String, index=True)
    full_name = Column(String, unique=True, index=True)
    url = Column(String)
    description = Column(Text, nullable=True)
    language = Column(String, nullable=True)
    stargazers_count = Column(Integer)
    tags = Column(String, nullable=True)
    kanboard_ticket_id = Column(Integer, nullable=True) # For now, a simple comma-separated string
