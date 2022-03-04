from sqlalchemy import create_engine, session_maker


class Database:
    def __init__(
        self,
        db_url: str,
        echo: bool = False,
        autocommit: bool = False,
        autoflush: bool = False,
    ):
        self._engine = create_engine(db_url, echo=echo)
        self._session = session_maker(
            bind=self._engine,
            autocommit=autocommit,
            autoflush=autoflush,
        )

    @property
    def session(self):
        return self._session

    def dispose(self):
        self._engine.dispose()


def get_db_session():
    db = Database()
    with db.session() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
