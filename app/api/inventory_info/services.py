from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.models import InventoryInfo as ModelInventoryInfo
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from api.inventory_info.schemas import PostInventoryInfo as ShemaPostInventoryInfo


async def list_inventory_info(session: AsyncSession) -> list[ModelInventoryInfo]:
    inventory_info = await session.execute(select(ModelInventoryInfo))
    return inventory_info.scalars().all()


async def get_inventory_info(uid: ModelInventoryInfo.uid, session: AsyncSession) -> ModelInventoryInfo:
    cour = await session.execute(select(ModelInventoryInfo).where(ModelInventoryInfo.uid == uid))
    inventory_info = cour.scalar_one_or_none()
    if inventory_info:
        return inventory_info
    raise HTTPException(status_code=404, detail="Inventory info not found")


async def create_inventory_info(inventory_info: ShemaPostInventoryInfo, session: AsyncSession) -> ModelInventoryInfo:
    inventory_info = ModelInventoryInfo(**inventory_info.dict())
    try:
        session.add(inventory_info)
        await session.commit()
        await session.refresh(inventory_info)
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Unique confict in inventory_info.')
    return inventory_info
