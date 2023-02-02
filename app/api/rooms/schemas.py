from uuid import UUID
from typing import Optional
from pydantic import BaseModel, root_validator
from fastapi.exceptions import HTTPException

from db.models.common import OrmModel


class PostRooms(OrmModel):
    floor: int
    number: str


class Rooms(PostRooms):
    uid: UUID


class PatchRooms(OrmModel):
    floor: Optional[int] = None
    number: Optional[str] = None

    @root_validator
    def check_empty(cls, v):
        if len(v) == 0:
            raise HTTPException(status_code=411, detail="Empty Json.")
        return v


class RoomNotFound404(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Room not found."},
        }


class RoomEmptyJson(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Empty Json."},
        }
