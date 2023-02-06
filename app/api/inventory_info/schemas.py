from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from db.models.common import OrmModel
from api.employee.schemas import Employee
from api.object_types.schemas import ObjectType


class InventoryInfo(OrmModel):
    uid: UUID
    name: str
    receipt_data: datetime | None = None
    model: str
    document: str
    date_of_registration: datetime | None = None
    cost: str
    useful_life: datetime | None = None
    note: str
    write_off_day: datetime | None = None
    inventory_number: str
    inventory_serial: str | None = None
    responsible: Employee
    object_type: ObjectType


class PostInventoryInfo(BaseModel):
    name: str
    receipt_data: datetime | None = None
    model: str
    document: str
    date_of_registration: datetime | None = None
    cost: str
    useful_life: datetime | None = None
    note: str
    write_off_day: datetime | None = None
    inventory_number: str
    inventory_serial: str | None = None
    responsible_uid: UUID | None = None
    object_types_uid: UUID | None = None
