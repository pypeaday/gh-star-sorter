from pydantic import BaseModel, Field
from typing import Optional


class RepositoryBase(BaseModel):
    repo_id: int = Field(alias='id')
    name: str
    full_name: str
    url: str = Field(alias='html_url')
    description: Optional[str] = None
    language: Optional[str] = None
    stargazers_count: int


class RepositoryCreate(RepositoryBase):
    pass


class Repository(RepositoryBase):
    id: int
    tags: Optional[str] = None

    class Config:
        from_attributes = True
