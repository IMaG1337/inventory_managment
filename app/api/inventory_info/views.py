from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from api.inventory_info import services
from api.inventory_info.schemas import (
    InventoryInfo as SchemaInventoryInfo,
    PostInventoryInfo as SchemaPostInventoryInfo
)


router = APIRouter(
    prefix="/inventory_info",
    tags=["inventory_info"]
)


@router.get("/", response_model=list[SchemaInventoryInfo])
async def list_inventory_info(session: AsyncSession = Depends(get_db)):
    list_inventory_info_models = await services.list_inventory_info(session)
    return list_inventory_info_models


@router.get("/{uid}", response_model=SchemaInventoryInfo)
async def get_inventory_info(uid: UUID, session: AsyncSession = Depends(get_db)):
    inventory_info_model = await services.get_inventory_info(uid, session)
    return inventory_info_model


@router.post("/", response_model=SchemaInventoryInfo)
async def create_inventory_info(inventory_info: SchemaPostInventoryInfo, session: AsyncSession = Depends(get_db)):
    inventory_info_model = await services.create_inventory_info(inventory_info, session)
    return inventory_info_model
