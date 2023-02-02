from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from api.departments import services
from api.departments.schemas import (
    Departments,
    PostDepartments,
    PatchDepartments,
    DepartmentsNotFound404,
    DepartmentsEmptyJson
)

router = APIRouter(
    prefix="/departments",
    tags=["departments"]
)


@router.get("/", response_model=Page[Departments])
async def list_department(session: AsyncSession = Depends(get_db)):
    department = await services.list_department(session)
    return department


@router.get(
    "/{uid}",
    response_model=Departments,
    responses={
        404: {
            "model": DepartmentsNotFound404,
            "description": "This endpoint is called if not found Department"
            }
        }
)
async def get_department(uid: UUID, session: AsyncSession = Depends(get_db)):
    department = await services.get_department(uid, session)
    return department


@router.post("/", response_model=Departments)
async def create_department(department: PostDepartments, session: AsyncSession = Depends(get_db)):
    department = await services.create_department(department, session)
    return department


@router.patch(
    "/{uid}",
    response_model=Departments,
    responses={
        411: {
            "model": DepartmentsEmptyJson,
            "description": "This endpoint is called if send empty Json."
        },
        404: {
            "model": DepartmentsNotFound404,
            "description": "This endpoint is called if Departments not found."
        }
    }
)
async def patch_department(uid: UUID, department_item: PatchDepartments, session: AsyncSession = Depends(get_db)):
    department = await services.patch_department(uid, department_item, session)
    return department
