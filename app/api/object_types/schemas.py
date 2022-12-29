from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from db.models.common import OrmModel


class PostObjectType(OrmModel):
    description: str


class ObjectType(PostObjectType):
    uid: UUID


class PatchObjectType(OrmModel):
    description: str


class ObjectTypeNotFound404(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "ObjectType not found."},
        }
