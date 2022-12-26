from uuid import UUID
from fastapi import APIRouter, Depends
from api.temp_inventory_card.schemas import (
    TempInventoryCard as SchemaTempInventoryCard,
    PostInventoryCard as SchemaPostInventoryCard,
    PostResponseInventoryCard as SchemaPostResponseInventoryCard
)
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from api.temp_inventory_card import services

router = APIRouter(
    prefix="/temp_inventory_card",
    tags=["temp inventory card"]
)


@router.get("/", response_model=list[SchemaTempInventoryCard] | list)
async def list_inventory_card(db: AsyncSession = Depends(get_db)):
    db_inventory_card = await services.list_temp_inventory_card(db)
    return db_inventory_card


@router.get("/{uid}", response_model=SchemaPostResponseInventoryCard)
async def create_inventory_card(uid: UUID, db: AsyncSession = Depends(get_db)):
    db_inventory_card = await services.get_temp_inventory_card(uid, db)
    return db_inventory_card


@router.post("/", response_model=SchemaPostResponseInventoryCard)
async def post_inventory_card(post_inventory_card: SchemaPostInventoryCard, db: AsyncSession = Depends(get_db)):
    db_inventory_card = await services.post_temp_inventory_card(db, post_inventory_card=post_inventory_card)
    return db_inventory_card
