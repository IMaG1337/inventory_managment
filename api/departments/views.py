from uuid import UUID
from fastapi import APIRouter, Depends
from api.departments.schemas import Departments, PostDepartments
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from api.departments import services

router = APIRouter()


@router.post("/departments/", response_model=Departments, tags=['departments'])
async def create_department(department: PostDepartments, session: AsyncSession = Depends(get_db)):
    department_model = await services.create_department(department, session)
    return department_model


@router.get("/departments/{uid}", response_model=Departments, tags=['departments'])
async def get_department(uid: UUID, session: AsyncSession = Depends(get_db)):
    db_department = await services.get_department(uid, session)
    return db_department


@router.get("/departments/", response_model=list[Departments] | list, tags=['departments'])
async def list_department(session: AsyncSession = Depends(get_db)):
    department_model = await services.list_department(session)
    return department_model
