from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.models.models import InventoryCard as ModelInventoryCard
from api.inventory_card.schemas import PostInventoryCard as SchemaPostInventoryCard


async def list_inventory_card(session: AsyncSession) -> list[ModelInventoryCard]:
    cour = await session.execute(select(ModelInventoryCard))
    list_inventory_card_models = cour.scalars().all()
    return list_inventory_card_models


async def get_inventory_card(uid: UUID, session: AsyncSession) -> ModelInventoryCard:
    inventory_card_model = await session.scalar(select(ModelInventoryCard).where(ModelInventoryCard.uid == uid))
    if inventory_card_model:
        return inventory_card_model
    raise HTTPException(404, detail='Not found inventory card.')


async def post_inventory_card(
    session: AsyncSession,
    post_inventory_card: SchemaPostInventoryCard
) -> list[ModelInventoryCard]:

    inventory_card_model = ModelInventoryCard(**post_inventory_card.dict())
    try:
        session.add(inventory_card_model)
        await session.commit()
        await session.refresh(inventory_card_model)
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Unique confict in inventory card.')
    return inventory_card_model
