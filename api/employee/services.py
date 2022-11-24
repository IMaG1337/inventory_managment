from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from db.models.models import Employee as ModelEmployee
from api.employee.schemas import PostEmployee as ShemaPostEmployee


async def create_employee(employee: ShemaPostEmployee, session: AsyncSession) -> ModelEmployee:
    employee_model = ModelEmployee(**employee.dict())
    try:
        session.add(employee_model)
        await session.commit()
        await session.refresh(employee_model)
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Unique confict in inventory_info.')
    return employee_model


async def list_employee(session: AsyncSession) -> list[ModelEmployee] | list:
    cour = await session.execute(select(ModelEmployee))
    return cour.scalars().all()


async def get_employee(uid: ModelEmployee.uid, session: AsyncSession) -> ModelEmployee:
    cour = await session.execute(select(ModelEmployee).where(ModelEmployee.uid == uid))
    employee = cour.scalar_one_or_none()
    if employee:
        return employee
    raise HTTPException(status_code=404, detail='Employee not found')
