from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page

from db.database import get_db
from api.object_types import services
from api.object_types.schemas import (
    ObjectType as SchemaObjectType,
    PostObjectType as SchemaPostObjectType,
    PatchObjectType as SchemaPatchObjectType,
    ObjectTypeNotFound404,
    ObjectTypeEmptyJson
)


router = APIRouter(
    prefix="/object_type",
    tags=["object_type"]
)


@router.get("/", response_model=Page[SchemaObjectType])
async def list_object_type(session: AsyncSession = Depends(get_db)):
    list_object_types = await services.list_object_types(session)
    return list_object_types


@router.get("/{uid}", response_model=SchemaObjectType)
async def get_object_type(uid: UUID, session: AsyncSession = Depends(get_db)):
    db_list_object_type = await services.get_object_type(uid, session)
    return db_list_object_type


@router.post("/", response_model=SchemaObjectType)
async def create_object_type(object_type: SchemaPostObjectType, session: AsyncSession = Depends(get_db)):
    object_type_model = await services.create_object_type(object_type, session)
    return object_type_model


@router.patch(
    "/{uid}",
    response_model=SchemaObjectType,
    responses={
        404: {
            "model": ObjectTypeNotFound404,
            "description": "This endpoint is called if not found ObjectType"
        },
        411: {
            "model": ObjectTypeEmptyJson,
            "description": "This endpoint is called if send empty Json."
        }
    }
)
async def patch_object_type(uid: UUID, object_type: SchemaPatchObjectType, session: AsyncSession = Depends(get_db)):
    object_type = await services.patch_object_type(uid, object_type, session)
    return object_type
