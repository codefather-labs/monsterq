import abc
from asyncio import AbstractEventLoop
from typing import Optional

from queue.callbacks import AbstractMessage


class AbstractConnection(abc.ABC):

    @property
    @abc.abstractmethod
    async def is_alive(self): ...

    @abc.abstractmethod
    async def close(self): ...


class AbstractQueueBackend(abc.ABC):
    loop: Optional[AbstractEventLoop] = None
    connection: AbstractConnection

    @abc.abstractmethod
    async def create_connection(self) -> AbstractConnection: ...

    @abc.abstractmethod
    async def close_connection(self) -> bool: ...

    @abc.abstractmethod
    async def send_message(self, message: AbstractMessage) -> bool: ...

    @abc.abstractmethod
    async def get_last_pending(self) -> AbstractMessage: ...
