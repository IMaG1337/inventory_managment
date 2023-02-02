from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from api.rooms import services
from api.rooms.schemas import (
    Rooms,
    PostRooms,
    PatchRooms,
    RoomNotFound404,
    RoomEmptyJson
)

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"]
)


@router.post("/", response_model=Rooms)
async def create_room(room: PostRooms, session: AsyncSession = Depends(get_db)):
    room_model = await services.create_room(room, session)
    return room_model


@router.patch(
    "/{uid}",
    response_model=Rooms,
    responses={
        404: {
            "model": RoomNotFound404,
            "description": "This endpoint is called if not found Room"
        },
        411: {
            "model": RoomEmptyJson,
            "description": "This endpoint is called if send empty Json."
        }
    }
)
async def patch_room(uid: UUID, room: PatchRooms, session: AsyncSession = Depends(get_db)):
    room_model = await services.patch_room(uid, room, session)
    return room_model


@router.get("/", response_model=list[Rooms] | list)
async def list_rooms(session: AsyncSession = Depends(get_db)):
    list_rooms = await services.list_rooms(session)
    return list_rooms


@router.get("/{uid}", response_model=Rooms)
async def get_room(uid: UUID, session: AsyncSession = Depends(get_db)):
    db_room = await services.get_room(uid, session)
    return db_room
