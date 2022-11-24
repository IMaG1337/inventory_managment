from uuid import UUID

from db.models.common import OrmModel
from api.rooms.schemas import Rooms
from api.departments.schemas import Departments


class Employee(OrmModel):
    uid: UUID
    name: str
    surname: str
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
