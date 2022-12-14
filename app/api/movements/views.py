from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from api.movements import services
from api.movements.schemas import (
        Movements as SchemaMovements,
        PostMovements as SchemaPostMovements,
        ResponsePostMovements as SchemaResponsePostMovements
    )

router = APIRouter(
    prefix="/movements",
    tags=["movements"]
)


@router.get("/", response_model=list[SchemaMovements] | list)
async def list_movements(session: AsyncSession = Depends(get_db)):
    list_movements = await services.list_movements(session)
    return list_movements


@router.get("/{uid}", response_model=SchemaMovements)
async def get_movements(uid: UUID, session: AsyncSession = Depends(get_db)):
    movements_model = await services.get_movements(uid, session)
    return movements_model


@router.post("/", response_model=SchemaResponsePostMovements)
async def create_movements(movements: SchemaPostMovements, session: AsyncSession = Depends(get_db)):
    movements_model = await services.create_movements(movements, session)
    return movements_model
