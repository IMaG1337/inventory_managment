from uuid import UUID

from db.models.common import OrmModel


class PostObjectType(OrmModel):
    description: str


class ObjectType(PostObjectType):
    uid: UUID
