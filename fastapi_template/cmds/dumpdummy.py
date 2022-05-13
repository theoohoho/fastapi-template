import click
from sqlalchemy.orm import Session

from fastapi_template.common.secure import get_password_hash
from fastapi_template.db import get_cmd_db_session
from fastapi_template.model import User

from .base import cmdjob


@cmdjob.command()
def dumpdummy(session: Session = get_cmd_db_session()):
    FAKE_USER_DB = {
        "johndoe": {
            "username": "johndoe@example.com",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "password": "fakeuser",
            "is_active": False,
        },
        "alice": {
            "username": "alice@example.com",
            "full_name": "Alice Wonderson",
            "email": "alice@example.com",
            "password": "fakeuser",
            "is_active": True,
        },
    }
    objs = []
    for key in FAKE_USER_DB:
        objs.append(
            User(
                full_name=FAKE_USER_DB[key]["full_name"],
                email=FAKE_USER_DB[key]["email"],
                hashed_password=get_password_hash(FAKE_USER_DB[key]["password"]),
                is_active=FAKE_USER_DB[key]["is_active"],
            )
        )

    with session as s:
        s.bulk_save_objects(objs)
