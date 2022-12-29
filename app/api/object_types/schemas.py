from uuid import UUID
from pydantic import BaseModel, root_validator
from fastapi.exceptions import HTTPException

from db.models.common import OrmModel


class PostObjectType(OrmModel):
    description: str


class ObjectType(PostObjectType):
    uid: UUID


class PatchObjectType(OrmModel):
    description: str

    @root_validator
    def check_empty(cls, v):
        if len(v) == 0:
            raise HTTPException(status_code=411, detail="Empty Json.")
        return v


class ObjectTypeNotFound404(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "ObjectType not found."},
        }


class ObjectTypeEmptyJson(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Empty Json."},
        }
