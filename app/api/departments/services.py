from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Page
from db.models.models import Departments as ModelDepartments
from api.departments.schemas import (
    PostDepartments as SchemaPostDepartments,
    Departments as SchemaDepartments
    )


async def create_department(department: SchemaPostDepartments, session: AsyncSession) -> ModelDepartments:
    department_model = ModelDepartments(**department.dict())
    session.add(department_model)
    await session.commit()
    await session.refresh(department_model)
    return department_model


async def patch_department(uid: UUID, department_item: SchemaDepartments, session: AsyncSession) -> SchemaDepartments:
    item = department_item.dict(exclude_unset=True)
    cour = await session.execute(
        update(ModelDepartments)
        .where(ModelDepartments.uid == uid)
        .values(**item)
        .returning(ModelDepartments)
        )
    await session.commit()
    result = cour.one_or_none()
    if result:
        return SchemaDepartments(**result)
    raise HTTPException(status_code=404, detail='Department not found.')


async def get_department(uid: UUID, session: AsyncSession) -> ModelDepartments:
    cour = await session.execute(select(ModelDepartments).where(ModelDepartments.uid == uid))
    department = cour.scalar_one_or_none()
    if department:
        return department
    raise HTTPException(status_code=404, detail='Department not found.')


async def list_department(session: AsyncSession) -> Page[ModelDepartments]:
    return await paginate(session, select(ModelDepartments))
