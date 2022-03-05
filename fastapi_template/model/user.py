from sqlalchemy import Boolean, Column, Integer, String
from fastapi_template.app.db.base import Base
from .mixin import CreateUpdateAtMixin


class User(CreateUpdateAtMixin, Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    is_active = Column(Boolean)
