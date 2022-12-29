from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi import HTTPException
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy import select, update

from db.models.models import ObjectTypes as ModelObjectTypes
from api.object_types.schemas import (
    PostObjectType as ShemaPostObjectType,
    PatchObjectType as SchemaPatchObjectType,
    ObjectType as SchemaObjectType)


async def create_object_type(object_type: ShemaPostObjectType, session: AsyncSession) -> ModelObjectTypes:
    object_type_model = ModelObjectTypes(**object_type.dict())
    session.add(object_type_model)
    await session.commit()
    await session.refresh(object_type_model)
    return object_type_model


async def list_object_types(session: AsyncSession) -> Page[ModelObjectTypes] | Page:
    return await paginate(session, select(ModelObjectTypes))


async def get_object_type(uid: ModelObjectTypes.uid, session: AsyncSession) -> ModelObjectTypes:
    object_type = await session.scalar(select(ModelObjectTypes).where(ModelObjectTypes.uid == uid))
    if object_type:
        return object_type
    raise HTTPException(status_code=404, detail='Object type not found')


async def patch_object_type(uid: UUID, object_type_item: SchemaPatchObjectType, session: AsyncSession):
    items = object_type_item.dict(exclude_unset=True)
    cour = await session.execute(
        update(ModelObjectTypes)
        .where(ModelObjectTypes.uid == uid)
        .values(**items)
        .returning(ModelObjectTypes)
        )
    object_type = cour.one_or_none()
    if object_type:
        return SchemaObjectType(**object_type)
    raise HTTPException(status_code=404, detail="ObjectType not found.")
