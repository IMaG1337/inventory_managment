from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from uuid import UUID

from db.models.models import Employee as ModelEmployee
from api.employee.schemas import PostEmployee as ShemaPostEmployee, PatchEmployee as SchemaPatchEmployee, Employee as SchemaEmpoloyee


async def create_employee(employee: ShemaPostEmployee, session: AsyncSession) -> ModelEmployee:
    employee_model = ModelEmployee(**employee.dict())
    try:
        session.add(employee_model)
        await session.commit()
        await session.refresh(employee_model)
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Unique confict in inventory_info.')
    return employee_model


async def patch_employee(uid: UUID, employee_item: SchemaPatchEmployee, session: AsyncSession) -> SchemaEmpoloyee:
    item = employee_item.dict(exclude_unset=True)
    await session.execute(
        update(ModelEmployee)
        .where(ModelEmployee.uid == uid)
        .values(**item)
        )
    await session.commit()
    cour = await session.scalars(select(ModelEmployee).where(ModelEmployee.uid == uid))
    employee = cour.one_or_none()
    return employee


async def list_employee(session: AsyncSession) -> list[ModelEmployee] | list:
    cour = await session.scalars(select(ModelEmployee))
    return cour.all()


async def get_employee(uid: ModelEmployee.uid, session: AsyncSession) -> ModelEmployee:
    cour = await session.scalars(select(ModelEmployee).where(ModelEmployee.uid == uid))
    employee = cour.one_or_none()
    await session.close()
    if employee:
        return employee
    raise HTTPException(status_code=404, detail='Employee not found')
