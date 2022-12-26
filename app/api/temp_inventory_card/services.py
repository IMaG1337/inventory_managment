from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.models.models import TempInventoryCard as ModelTempInventoryCard
from fastapi import HTTPException
from api.inventory_card.schemas import PostInventoryCard as SchemaPostInventoryCard


async def list_temp_inventory_card(session: AsyncSession) -> list[ModelTempInventoryCard]:
    cour = await session.execute(select(ModelTempInventoryCard))
    list_inventory_card_models = cour.scalars().all()
    return list_inventory_card_models


async def get_temp_inventory_card(uid: ModelTempInventoryCard.uid, session: AsyncSession) -> ModelTempInventoryCard:
    cour = await session.execute(select(ModelTempInventoryCard).where(ModelTempInventoryCard.uid == uid))
    inventory_card_model = cour.scalar_one_or_none()
    if inventory_card_model:
        return inventory_card_model
    raise HTTPException(404, detail='Not found inventory card.')


async def post_temp_inventory_card(
    session: AsyncSession,
    post_inventory_card: SchemaPostInventoryCard
) -> ModelTempInventoryCard:

    inventory_card_model = ModelTempInventoryCard(**post_inventory_card.dict())
    try:
        session.add(inventory_card_model)
        await session.commit()
        await session.refresh(inventory_card_model)
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Unique confict in inventory card.')
    return inventory_card_model
