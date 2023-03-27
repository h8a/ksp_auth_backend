import uuid

import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import select


SAModel = declarative_base()


class Base(object):

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    create_date = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    status      = sa.Column(sa.String(2), default='1')

    @classmethod
    async def get(cls, session, **kwargs):
        result = None

        async with session.begin():
            query = select(cls).filter_by(**kwargs)
            result = (await session.execute(query)).scalars()
            result = result.first()

        return result

    async def save(self, session):
        async with session.begin():
            session.add(self)
            await session.flush()
            await session.refresh(self, attribute_names=['id'])
            await session.commit()

        return self


class UsersModel(SAModel, Base):

    __tablename__ = 'users'

    username = sa.Column(sa.String(50), unique=True, nullable=False)
    password = sa.Column(sa.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
