from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from api.inventory_card import services
from api.inventory_card.schemas import (
    InventoryCard as SchemaInventoryCard,
    PostInventoryCard as SchemaPostInventoryCard,
    PostResponseInventoryCard as SchemaPostResponseInventoryCard
)

router = APIRouter()


@router.get("/inventory_card/", response_model=list[SchemaInventoryCard] | list, tags=['inventory_card'])
async def list_inventory_card(db: AsyncSession = Depends(get_db)):
    db_inventory_card = await services.list_inventory_card(db)
    return db_inventory_card


@router.get("/inventory_card/{uid}", response_model=SchemaInventoryCard, tags=['inventory_card'])
async def create_inventory_card(uid: UUID, db: AsyncSession = Depends(get_db)):
    db_inventory_card = await services.create_inventory_card(uid, db)
    return db_inventory_card


@router.post("/inventory_card/", response_model=SchemaPostResponseInventoryCard, tags=['inventory_card'])
async def post_inventory_card(post_inventory_card: SchemaPostInventoryCard, db: AsyncSession = Depends(get_db)):
    db_inventory_card = await services.post_inventory_card(db, post_inventory_card=post_inventory_card)
    return db_inventory_card
