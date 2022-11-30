from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from db.models.models import Rooms as ModelRoom
from api.rooms.schemas import (
    PostRooms as SchemaPostRoom,
    Rooms as SchemaRoom)


async def list_rooms(session: AsyncSession) -> list[ModelRoom]:
    cour = await session.execute(select(ModelRoom))
    result = cour.scalars().all()
    return result


async def get_room(uid: UUID, session: AsyncSession) -> ModelRoom:
    cour = await session.execute(select(ModelRoom).where(ModelRoom.uid == uid))
    room = cour.scalar_one_or_none()
    if room:
        return room
    raise HTTPException(status_code=404, detail='Room not found.')


async def create_room(room: SchemaPostRoom, session: AsyncSession) -> ModelRoom:
    room_model = ModelRoom(**room.dict())
    try:
        session.add(room_model)
        await session.commit()
        await session.refresh(room_model)
        return room_model
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Room already exist.')


async def patch_room(uid: UUID, room_item: SchemaRoom, session: AsyncSession) -> SchemaRoom:
    item = room_item.dict(exclude_unset=True)
    cour = await session.execute(
        update(ModelRoom)
        .where(ModelRoom.uid == uid)
        .values(**item).returning(ModelRoom)
        )
    room = SchemaRoom(**cour.fetchone())
    await session.commit()
    return room
