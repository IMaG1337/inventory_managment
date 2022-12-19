from uuid import UUID
from typing import Optional

from db.models.common import OrmModel
from api.rooms.schemas import Rooms
from api.departments.schemas import Departments


class Employee(OrmModel):
    uid: UUID
    name: str
    surname: str
    fullname: str
    patronymicon: str | None = None
    position: str
    status: str
    department: Departments
    room: Rooms


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
