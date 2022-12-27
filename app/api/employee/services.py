from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi_pagination.ext.async_sqlalchemy import paginate

from db.models.models import Employee as ModelEmployee
from api.employee.schemas import (
    PostEmployee as ShemaPostEmployee,
    PatchEmployee as SchemaPatchEmployee,
    Employee as SchemaEmpoloyee
    )


async def create_employee(employee: ShemaPostEmployee, session: AsyncSession) -> SchemaEmpoloyee:
    employee_model = ModelEmployee(**employee.dict())
    try:
        session.add(employee_model)
        await session.commit()
        await session.refresh(employee_model)
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Unique confict in inventory_info.')
    return SchemaEmpoloyee(**employee_model.__dict__)


async def patch_employee(uid: UUID, employee_item: SchemaPatchEmployee, session: AsyncSession) -> SchemaEmpoloyee:
    items = employee_item.dict(exclude_unset=True)
    cour = await session.execute(
        update(ModelEmployee)
        .where(ModelEmployee.uid == uid)
        .values(**items)
        .returning(ModelEmployee))
    employee_dict = cour.mappings().fetchone()
    return SchemaPatchEmployee(**employee_dict)


async def list_employee(session: AsyncSession) -> list[ModelEmployee] | list:
    return await paginate(session, select(ModelEmployee))


async def get_employee(uid: ModelEmployee.uid, session: AsyncSession) -> SchemaEmpoloyee:
    employee: ModelEmployee = await session.scalar(select(ModelEmployee).where(ModelEmployee.uid == uid))
    if employee:
        return employee
    raise HTTPException(status_code=404, detail='Employee not found')
