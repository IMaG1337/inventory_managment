from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_pagination.ext.async_sqlalchemy import paginate
from db.models.models import InventoryInfo as ModelInventoryInfo
from sqlalchemy.exc import IntegrityError, DBAPIError
from fastapi import HTTPException
from fastapi_pagination import Page
from api.inventory_info.schemas import (
    PostInventoryInfo as ShemaPostInventoryInfo,
    InventoryInfo as ShemaInventoryInfo
    )


async def list_inventory_info(session: AsyncSession) -> Page[ShemaInventoryInfo]:
    return await paginate(session, select(ModelInventoryInfo))


async def get_inventory_info(uid: ModelInventoryInfo.uid, session: AsyncSession) -> ModelInventoryInfo:
    inventory_info = await session.scalar(select(ModelInventoryInfo).where(ModelInventoryInfo.uid == uid))
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
    except DBAPIError:
        raise HTTPException(status_code=400, detail='Bad Data exception.')
    return inventory_info
