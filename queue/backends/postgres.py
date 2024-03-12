import base64
import os
import pickle
from asyncio import AbstractEventLoop
from typing import Optional, List, Callable, Any

import asyncpg

from queue.backends.callbacks import PostgresCallback, PostgresMessage
from queue.callbacks import AbstractMessage
from queue.interfaces import AbstractQueueBackend, AbstractConnection


class BasePostgresConnection(AbstractConnection):

    def __init__(self, loop: AbstractEventLoop):
        self.connection_data = {
            "user": os.environ.get("POSTGRES_USER", "postgres"),
            "password": os.environ.get("POSTGRES_PASS", "task_manager_password"),
            "database": os.environ.get("POSTGRES_NAME", "task_manager"),
            "host": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
            "port": os.environ.get("POSTGRES_PORT", "5432"),
        }
        self.connection: Optional[asyncpg.Connection] = None

    async def create_connection(self):
        self.connection = await asyncpg.connect(**self.connection_data)
        return self.connection

    @property
    def is_alive(self):
        return not self.connection.is_closed() if self.connection else False

    async def close(self):
        await self.connection.close()

    async def add_listener(self, topic: str, callback: Callable):
        await self.connection.add_listener(topic, callback)


class PostgresBackend(AbstractQueueBackend):

    def __init__(self, autoconnect: bool = True):
        self.connection: Optional[BasePostgresConnection] = None
        if autoconnect:
            self.loop.create_task(
                self.create_connection()
            )
        self.callback_list: List[PostgresCallback] = []

    async def create_connection(self) -> BasePostgresConnection:
        self.connection: BasePostgresConnection = BasePostgresConnection(loop=self.loop)
        await self.connection.create_connection()
        return self.connection

    async def close_connection(self) -> bool:
        await self.connection.close()
        return True

    async def send_message(self, message: PostgresMessage) -> bool:
        # TODO insert into table
        # TODO message.topic

        await self.connection.connection.execute(
            f"NOTIFY tasks, '{await message.serialize()}'"
        )
        return True

    async def get_last_pending(self) -> PostgresMessage:
        # TODO impl
        pass
