from uuid import UUID
from db.models.common import OrmModel
from typing import Optional


class PostRooms(OrmModel):
    floor: int
    number: str


class Rooms(PostRooms):
    uid: UUID


class PatchRoom(OrmModel):
    floor: Optional[int] = None
    number: Optional[str] = None
