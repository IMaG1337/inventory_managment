from uuid import UUID
from fastapi import APIRouter, Depends
from api.object_types.schemas import (
    ObjectType as SchemaObjectType,
    PostObjectType as SchemaPostObjectType
)
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from api.object_types import services


router = APIRouter()


@router.get("/object_type/", response_model=list[SchemaObjectType], tags=['object_type'])
async def list_object_type(session: AsyncSession = Depends(get_db)):
    list_object_types = await services.list_object_types(session)
    return list_object_types


@router.get("/object_type/{uid}", response_model=SchemaObjectType, tags=['object_type'])
async def get_object_type(uid: UUID, session: AsyncSession = Depends(get_db)):
    db_list_object_type = await services.get_object_type(uid, session)
    return db_list_object_type


@router.post("/object_type/", response_model=SchemaObjectType, tags=['object_type'])
async def create_object_type(object_type: SchemaPostObjectType, session: AsyncSession = Depends(get_db)):
    object_type_model = await services.create_object_type(object_type, session)
    return object_type_model
