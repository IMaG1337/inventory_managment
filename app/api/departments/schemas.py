from fastapi.exceptions import HTTPException
from uuid import UUID
from pydantic import BaseModel, root_validator

from db.models.common import OrmModel


class PostDepartments(OrmModel):
    name: str


class Departments(PostDepartments):
    uid: UUID


class PatchDepartments(OrmModel):
    name: str

    @root_validator(pre=True)
    def check_empty(cls, v):
        if len(v) == 0:
            raise HTTPException(status_code=411, detail="Empty json")
        return v


class DepartmentsNotFound404(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Department not found."},
        }


class DepartmentsEmptyJson(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Empty json."},
        }
