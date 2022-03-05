from sqlalchemy import Boolean, Column, Integer, String

from fastapi_template.db import Base

from .mixins import CreateUpdateAtMixin


class User(CreateUpdateAtMixin, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
