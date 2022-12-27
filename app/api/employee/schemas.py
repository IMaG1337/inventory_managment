from uuid import UUID
from typing import Optional

from db.models.common import OrmModel
from api.rooms.schemas import PostRooms
from api.departments.schemas import PostDepartments


class Employee(OrmModel):
    uid: UUID
    name: str
    surname: str
    patronymicon: str | None = None
    fullname: str
    position: str
    status: str
    department: PostDepartments
    room: PostRooms


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
