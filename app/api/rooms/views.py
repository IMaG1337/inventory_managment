from uuid import UUID
from fastapi import APIRouter, Depends
from api.rooms.schemas import Rooms, PostRooms, PatchRoom
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from api.rooms import services

router = APIRouter()


@router.post("/rooms/", response_model=Rooms, tags=['rooms'])
async def create_room(room: PostRooms, session: AsyncSession = Depends(get_db)):
    room_model = await services.create_room(room, session)
    return room_model


@router.patch("/rooms/{uid}", response_model=Rooms, tags=['rooms'])
async def patch_room(uid: UUID, room: PatchRoom, session: AsyncSession = Depends(get_db)):
    room_model = await services.patch_room(uid, room, session)
    return room_model


@router.get("/rooms/", response_model=list[Rooms] | list, tags=['rooms'])
async def list_rooms(session: AsyncSession = Depends(get_db)):
    list_rooms = await services.list_rooms(session)
    return list_rooms


@router.get("/rooms/{uid}", response_model=Rooms, tags=['rooms'])
async def get_room(uid: UUID, session: AsyncSession = Depends(get_db)):
    db_room = await services.get_room(uid, session)
    return db_room
