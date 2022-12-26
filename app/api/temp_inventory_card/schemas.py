from uuid import UUID
from db.models.common import OrmModel
from api.employee.schemas import Employee
from api.rooms.schemas import Rooms


class TempInventoryCard(OrmModel):
    uid: UUID
    employee: Employee
    room: Rooms
    inventory_card_uid: UUID


class PostInventoryCard(OrmModel):
    employee_uid: UUID
    inventory_card_uid: UUID
    room_uid: UUID


class PostResponseInventoryCard(PostInventoryCard):
    uid: UUID
