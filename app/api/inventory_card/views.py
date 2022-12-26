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

router = APIRouter(
    prefix="/inventory_card",
    tags=["inventory_card"]
)


@router.get("/", response_model=list[SchemaInventoryCard] | list)
async def list_inventory_card(db: AsyncSession = Depends(get_db)):
    db_inventory_card = await services.list_inventory_card(db)
    return db_inventory_card


@router.get("/{uid}", response_model=SchemaInventoryCard)
async def get_inventory_card(uid: UUID, db: AsyncSession = Depends(get_db)):
    db_inventory_card = await services.get_inventory_card(uid, db)
    return db_inventory_card


@router.post("/", response_model=SchemaPostResponseInventoryCard)
async def post_inventory_card(post_inventory_card: SchemaPostInventoryCard, db: AsyncSession = Depends(get_db)):
    db_inventory_card = await services.post_inventory_card(db, post_inventory_card=post_inventory_card)
    return db_inventory_card
