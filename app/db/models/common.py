from pydantic import BaseModel


class OrmModel(BaseModel):

    class Config:
        orm_mode = True
