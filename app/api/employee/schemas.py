from uuid import UUID
from typing import Optional
from pydantic import BaseModel, root_validator
from fastapi.exceptions import HTTPException

from db.models.common import OrmModel
from api.rooms.schemas import PostRooms
from api.departments.schemas import PostDepartments


class Employee(OrmModel):
    uid: UUID
    name: str
    surname: str
    # patronymicon: str | None = None
    # fullname: str
    # position: str
    # status: str
    # department: PostDepartments
    # room: PostRooms


class PostEmployee(OrmModel):
    name: str
    surname: str
    patronymicon: str | None = None
    position: str
    status: str
    departments_uid: UUID
    room_uid: UUID


class PatchEmployee(OrmModel):
    name: Optional[str] | None = None
    surname: Optional[str] | None = None
    patronymicon: Optional[str] | None = None
    position: Optional[str] | None = None
    status: Optional[str] | None = None
    departments_uid: Optional[UUID] | None = None
    room_uid: Optional[UUID] | None = None

    @root_validator(pre=True)
    def check_empty(cls, v):
        if len(v) == 0:
            raise HTTPException(status_code=411, detail="Empty Json.")
        return v


class EmployeeNotFound404(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Employee not found."},
        }


class EmployeeEmptyJson(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Empty Json."},
        }
