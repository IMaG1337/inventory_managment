from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from api.inventory_info import services
from api.inventory_info.schemas import (
    InventoryInfo as SchemaInventoryInfo,
    PostInventoryInfo as SchemaPostInventoryInfo
)


router = APIRouter()


@router.get("/inventory_info/", response_model=list[SchemaInventoryInfo], tags=['inventory_info'])
async def list_inventory_info(session: AsyncSession = Depends(get_db)):
    list_inventory_info_models = await services.list_inventory_info(session)
    return list_inventory_info_models


@router.get("/inventory_info/{uid}", response_model=SchemaInventoryInfo, tags=['inventory_info'])
async def get_inventory_info(uid: UUID, session: AsyncSession = Depends(get_db)):
    inventory_info_model = await services.get_inventory_info(uid, session)
    return inventory_info_model


@router.post("/inventory_info/", response_model=SchemaInventoryInfo, tags=['inventory_info'])
async def create_inventory_info(inventory_info: SchemaPostInventoryInfo, session: AsyncSession = Depends(get_db)):
    inventory_info_model = await services.create_inventory_info(inventory_info, session)
    return inventory_info_model