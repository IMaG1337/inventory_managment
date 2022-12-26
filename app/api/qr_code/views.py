from io import BytesIO
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from api.qr_code.schemas import QRcodeSchema
from api.qr_code import services


router = APIRouter(
    prefix="/qr_code",
    tags=['QR code']
)


@router.post('/', responses={
    201: {
        'description':
            "Create svg qr-code",
        "content": {
            "image/svg+xml": {}
            }
        }
    }
)
async def create_qr_code(data: QRcodeSchema):
    qrcode_data = await services.create_qr_code(data)
    headers = {
        "Content-Disposition": f'attachment; filename="QRcode_{data.type}.svg"',
        "Content-Type": "image/svg+xml"
        }
    stream = BytesIO()
    qrcode_data.save(stream)  # save our svg image in memory
    content = stream.getvalue().decode()  # xml string
    return HTMLResponse(content=content, headers=headers, status_code=201)
