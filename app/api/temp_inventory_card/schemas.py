from uuid import UUID
from db.models.common import OrmModel
from api.employee.schemas import Employee
from api.rooms.schemas import Rooms
from api.inventory_info.schemas import InventoryInfo


class TempInventoryCard(OrmModel):
    uid: UUID
    employee: Employee
    inventory_info: InventoryInfo
    room: Rooms


class PostInventoryCard(OrmModel):
    employee_uid: UUID
    inventory_info_uid: UUID
    room_uid: UUID


class PostResponseInventoryCard(PostInventoryCard):
    uid: UUID
