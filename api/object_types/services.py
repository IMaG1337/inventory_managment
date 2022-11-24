from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.models import ObjectTypes as ModelObjectTypes
from fastapi import HTTPException
from api.object_types.schemas import PostObjectType as ShemaPostObjectType


async def create_object_type(object_type: ShemaPostObjectType, session: AsyncSession) -> ModelObjectTypes:
    object_type_model = ModelObjectTypes(**object_type.dict())
    session.add(object_type_model)
    await session.commit()
    await session.refresh(object_type_model)
    return object_type_model


async def list_object_types(session: AsyncSession) -> ModelObjectTypes:
    list_object_types = await session.execute(select(ModelObjectTypes))
    return list_object_types.scalars().all()


async def get_object_type(uid: ModelObjectTypes.uid, session: AsyncSession) -> ModelObjectTypes:
    cour = await session.execute(select(ModelObjectTypes).where(ModelObjectTypes.uid == uid))
    object_type = cour.scalar_one_or_none()
    if object_type:
        return object_type
    raise HTTPException(status_code=404, detail='Object type not found')
