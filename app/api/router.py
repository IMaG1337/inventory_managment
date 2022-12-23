from fastapi.routing import APIRouter

from api.rooms.views import router as room_router
from api.employee.views import router as employee_router
from api.departments.views import router as departments_router
from api.object_types.views import router as object_types_router
from api.inventory_info.views import router as inventory_info_router
from api.inventory_card.views import router as inventory_card_router
from api.movements.views import router as movements_router
from api.inventory_table.views import router as inventory_table_router
from api.qr_code.views import router as qrcode

api_router = APIRouter()
api_router.include_router(room_router)
api_router.include_router(departments_router)
api_router.include_router(employee_router)
api_router.include_router(object_types_router)
api_router.include_router(inventory_info_router)
api_router.include_router(inventory_card_router)
api_router.include_router(movements_router)
api_router.include_router(inventory_table_router)
api_router.include_router(qrcode)

