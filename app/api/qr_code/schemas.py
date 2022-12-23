from pydantic import BaseModel
from uuid import UUID


class QRcodeSchema(BaseModel):
    type: str
    uid: UUID
