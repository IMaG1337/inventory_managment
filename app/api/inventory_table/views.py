from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from api.inventory_table import services
from api.inventory_table.schemas import ListInventoryTable

router = APIRouter(
    prefix="/inventory/table",
    tags=['inventory table']
)


@router.get("/", response_model=ListInventoryTable | list)
async def list_inventory_table(db: AsyncSession = Depends(get_db)):
    list_inventory_table = await services.list_inventory_table(db)
    return list_inventory_table
