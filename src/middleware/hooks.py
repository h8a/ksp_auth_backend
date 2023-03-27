import logging

from db.manager import DBManager


class HookDBMiddleware(object):

    def __init__(self, connection: str):
        self.connection = connection

    async def process_startup(self, scope, event):
        manager = DBManager(self.connection)
        await manager.create_all()
