from uuid import UUID
from db.models.common import OrmModel


class InventoryTable(OrmModel):
    uid: UUID
    temp: bool
    model: str
    name: str
    inventory_serial: str
    inventory_number: str
    employee_fullname: str
    employee_uid: UUID
    responsible_fullname: str
    responsible_uid: UUID


class ListInventoryTable(OrmModel):
    __root__: list[InventoryTable]
