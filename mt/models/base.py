from datetime import datetime as dt

from sqlalchemy import (
    Column,
    Unicode,
    DateTime,
    inspect
)
from sqlalchemy.event import listens_for
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from mt.lib.helpers import uuid4hex
from mt.models.db import Base


class BaseModel(Base):
    __abstract__ = True
    excluded_hybrid_properties = ()

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    id = Column(Unicode, primary_key=True, default=uuid4hex)

    _created_at = Column(DateTime, default=dt.now)
    _updated_at = Column(DateTime, default=dt.now)
    _deleted_at = Column(DateTime, nullable=True)

    @classmethod
    def query(cls, session):
        # This is a result of an sqla quirk. sqla requires an sql expression for filter().
        # is False will not work here because a column (hybrid property in this case) is not None.
        # Its value is. And we can't use .is_(False) as it's a hybrid prop and it doesn't support it.
        # noinspection PyComparisonWithNone
        return session.query(cls).filter(cls.deleted == False)

    @classmethod
    def query_with_deleted(cls, session):
        return session.query(cls)

    @hybrid_property
    def created_at(self):
        return self._created_at

    @hybrid_property
    def deleted_at(self):
        return self._deleted_at

    @hybrid_property
    def updated_at(self):
        return self._updated_at

    # noinspection PyComparisonWithNone
    @hybrid_property
    def deleted(self):
        # sqla can't override the is operator and we need to return an sql statement here.
        return self._deleted_at != None

    @property
    def as_dict(self):
        # XXX: this might somehow be suboptimal
        inspected = inspect(self.__class__)
        ret = {}

        for column in inspected.mapper.column_attrs:
            key = column.key
            # exclude 'private' column attrs
            if key[0] != '_':
                ret[key] = getattr(self, key)

        for descriptor in inspected.all_orm_descriptors:
            if type(descriptor) == hybrid_property and descriptor.__name__ not in self.excluded_hybrid_properties:
                ret[descriptor.__name__] = getattr(self, descriptor.__name__)

        return ret

    def soft_delete(self):
        self._deleted_at = dt.now()


@listens_for(BaseModel, "before_update", propagate=True)
def update_updated_at(_, __, target):
    target._updated_at = dt.now()
