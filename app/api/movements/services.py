from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from db.models.models import Movements as ModelMovements
from api.movements.schemas import PostMovements as SchemaPostMovements


async def list_movements(session: AsyncSession) -> list[ModelMovements] | list:
    list_movements = await session.execute(select(ModelMovements))
    return list_movements.scalars().all()


async def get_movements(uid: UUID, session: AsyncSession) -> ModelMovements:
    cour = await session.execute(select(ModelMovements).where(ModelMovements.uid == uid))
    movements_model = cour.scalar_one_or_none()
    if movements_model:
        return movements_model
    raise HTTPException(status_code=404, detail='Movements not found.')


async def create_movements(movements: SchemaPostMovements, session: AsyncSession) -> ModelMovements:
    movements_model = ModelMovements(**movements.dict())
    try:
        session.add(movements_model)
        await session.commit()
        await session.refresh(movements_model)
        return movements_model
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Movements already exist.')
