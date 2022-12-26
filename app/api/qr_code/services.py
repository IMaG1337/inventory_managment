import qrcode
import qrcode.image.svg
from api.qr_code.schemas import QRcodeSchema


async def create_qr_code(qr_code_data: QRcodeSchema) -> qrcode.image.svg.SvgImage:
    factory = qrcode.image.svg.SvgImage
    qr_code = qrcode.make(f'{qr_code_data.type};{str(qr_code_data.uid)}', image_factory=factory)
    return qr_code
