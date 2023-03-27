import logging
from asyncio import current_task

from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    create_async_engine)
from sqlalchemy.orm.session import sessionmaker

from db import models


class DBManager(object):

    def __init__(self, connection: str, debug=False):
        self.connection = connection

        self.engine = create_async_engine(
            self.connection,
            connect_args={'timeout': 60},
            echo=debug,
        )
        self.DBSession = async_scoped_session(
            session_factory=sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            scopefunc=current_task
        )

    @property
    def session(self):
        return self.DBSession()

    async def create_all(self):
        async with self.engine.begin() as conn:
            try:
                await conn.run_sync(models.SAModel.metadata.create_all)
                logging.getLogger('db').info('DB created or validated')
            except Exception:
                logging.getLogger('db').error('Could not initialize DB', exc_info=True)
