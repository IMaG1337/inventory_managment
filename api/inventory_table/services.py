from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import text, label
from sqlalchemy.orm import aliased

from api.inventory_table.schemas import ListInventoryTable
from db.models.models import (
        InventoryCard as ModelInventoryCard,
        InventoryInfo as ModelInventoryInfo,
        TempInventoryCard as ModelTempInventoryCard,
        Employee as ModelEmployee
        )


async def list_inventory_table(session: AsyncSession) -> ListInventoryTable:
    employee = aliased(ModelEmployee)
    responsible = aliased(ModelEmployee)
    temp = select(text('1')).where(
            ModelInventoryCard.uid == ModelTempInventoryCard.inventory_card_uid).exists().label('temp')
    selecting = select(
            ModelInventoryCard.uid,
            temp,
            label('employee_fullname', employee.fullname),
            label('employee_uid', employee.uid),
            label('responsible_fullname', responsible.fullname),
            label('responsible_uid', responsible.uid),
            label('inventory_number_uid', ModelInventoryInfo.uid),
            label('model', ModelInventoryInfo.model),
            label('inventory_number', ModelInventoryInfo.inventory_number),
            label('name', ModelInventoryInfo.name),
            label('inventory_serial', ModelInventoryInfo.inventory_serial))\
        .join(employee, employee.uid == ModelInventoryCard.employee_uid)\
        .join(ModelInventoryInfo, ModelInventoryCard.inventory_info_uid == ModelInventoryInfo.uid)\
        .join(responsible, responsible.uid == ModelInventoryInfo.responsible_uid)
    cour = await session.execute(selecting)
    data = cour.mappings().all()
    result = ListInventoryTable(__root__=data)
    return result
