from sqlalchemy import (
    Column,
    Unicode,
    Boolean
)

from mt.models.base import BaseModel


class User(BaseModel):
    email = Column(Unicode, unique=True)
    name = Column(Unicode(127))
    is_admin = Column(Boolean, default=False)
