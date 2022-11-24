from uuid import UUID
from db.models.common import OrmModel


class PostRooms(OrmModel):
    floor: int
    number: str


class Rooms(PostRooms):
    uid: UUID
