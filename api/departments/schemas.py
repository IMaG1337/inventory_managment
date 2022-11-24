from uuid import UUID
from db.models.common import OrmModel


class PostDepartments(OrmModel):
    name: str


class Departments(PostDepartments):
    uid: UUID
