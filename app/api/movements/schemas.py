from datetime import datetime
from uuid import UUID
from db.models.common import OrmModel
from api.employee.schemas import Employee
from api.inventory_card.schemas import InventoryCard


class PostMovements(OrmModel):
    reason: str
    from_employee_uid: UUID
    to_employee_uid: UUID
    inventory_card_uid: UUID


class ResponsePostMovements(PostMovements):
    uid: UUID


class Movements(OrmModel):
    uid: UUID
    date: datetime
    reason: str
    from_employee: Employee
    to_employee: Employee
    inventory_card: InventoryCard
