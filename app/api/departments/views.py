from uuid import UUID
from fastapi import APIRouter, Depends
from api.departments.schemas import Departments, PostDepartments, PatchDepartments
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page
from db.database import get_db
from api.departments import services

router = APIRouter(
    prefix="/departments",
    tags=["departments"]
)


@router.get("/", response_model=Page[Departments])
async def list_department(session: AsyncSession = Depends(get_db)):
    department_model = await services.list_department(session)
    return department_model


@router.get("/{uid}", response_model=Departments)
async def get_department(uid: UUID, session: AsyncSession = Depends(get_db)):
    department_model = await services.get_department(uid, session)
    return department_model


@router.post("/", response_model=Departments)
async def create_department(department: PostDepartments, session: AsyncSession = Depends(get_db)):
    department_model = await services.create_department(department, session)
    return department_model


@router.patch("/{uid}", response_model=Departments, responses={408: {'description': 'test'}})
async def patch_department(uid: UUID, department_item: PatchDepartments, session: AsyncSession = Depends(get_db)):
    department_model = await services.patch_department(uid, department_item, session)
    return department_model
