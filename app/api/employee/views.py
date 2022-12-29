from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from api.employee.schemas import (
    Employee as SchemaEmloyee,
    PostEmployee as SchemaPostEmployee,
    PatchEmployee as SchemaPatchEmployee,
    EmployeeNotFound404,
    EmployeeEmptyJson
)
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from api.employee import services


router = APIRouter(
    prefix="/employee",
    tags=["employee"]
)


@router.get("/", response_model=Page[SchemaEmloyee])
async def list_employee(db: AsyncSession = Depends(get_db)):
    list_employee = await services.list_employee(db)
    return list_employee


@router.get(
    "/{uid}",
    response_model=SchemaEmloyee,
    responses={
        404: {
            "model": EmployeeNotFound404,
            "description": "This endpoint is called if not found Employee"
        }
    }
)
async def get_employee(uid: UUID, db: AsyncSession = Depends(get_db)):
    employee = await services.get_employee(uid, db)
    return employee


@router.post("/", response_model=SchemaEmloyee)
async def create_employee(employee: SchemaPostEmployee, session: AsyncSession = Depends(get_db)):
    db_employee = await services.create_employee(employee, session)
    return db_employee


@router.patch(
    "/{uid}",
    response_model=SchemaPatchEmployee,
    responses={
        404: {
            "model": EmployeeNotFound404,
            "description": "This endpoint is called if not found Employee."
        },
        411: {
            "model": EmployeeEmptyJson,
            "description": "This endpoint is called if send empty Json."
        }
    }
)
async def patch_employee(uid: UUID, employee: SchemaPatchEmployee, session: AsyncSession = Depends(get_db)):
    db_employee = await services.patch_employee(uid, employee, session)
    return db_employee
