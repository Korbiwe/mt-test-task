__all__ = ['Database', 'Base']
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Database:
    def __init__(self, db_url, clear_on_teardown):
        self.clear_on_teardown = clear_on_teardown
        self.engine = create_engine(db_url)
        self._factory = sessionmaker(bind=self.engine)

    def __del__(self):
        if self.clear_on_teardown:
            Base.metadata.drop_all(bind=self.engine)

    def new_session(self):
        Base.metadata.create_all(self.engine)
        return self._factory()

    @contextmanager
    def session_context(self):
        session = self.new_session()
        try:
            yield session
            session.commit()
        except BaseException:
            session.rollback()
            raise
        finally:
            session.close()
