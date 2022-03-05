from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_template.core.settings import get_settings


class Database:
    def __init__(
        self,
        db_url: str,
        echo: bool = False,
        autocommit: bool = False,
        autoflush: bool = False,
    ):
        self._engine = create_engine(db_url, echo=echo)
        self._session = sessionmaker(
            bind=self._engine,
            autocommit=autocommit,
            autoflush=autoflush,
        )

    @property
    def session(self):
        return self._session

    def dispose(self):
        self._engine.dispose()


def get_db_session(settings=get_settings()):
    db = Database(db_url=settings.database.db_url)
    with db.session() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.commit()
