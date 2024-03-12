import abc
from typing import List

from queue.backends.postgres import BasePostgresConnection
from queue.callbacks import AbstractCallback, AbstractMessage
from queue.interfaces import AbstractQueueBackend, AbstractConnection


class ISubscriberEventCallback(abc.ABC):
    callback_list: List[AbstractCallback]

    @abc.abstractmethod
    async def on_event_callback(self): ...


class ISubscriber(AbstractConnection):
    connection: BasePostgresConnection

    @abc.abstractmethod
    async def set_subscription_callback_list(
            self,
            topic: str,
            callback_list: List[AbstractCallback],
    ): ...

    @property
    @abc.abstractmethod
    async def is_alive(self): ...

    @abc.abstractmethod
    async def close(self): ...

    @abc.abstractmethod
    async def pop(self) -> AbstractMessage: ...


class IPublisher(AbstractConnection):
    connection: BasePostgresConnection

    @property
    @abc.abstractmethod
    async def is_alive(self): ...

    @abc.abstractmethod
    async def close(self): ...

    @abc.abstractmethod
    async def push(self, message: AbstractMessage) -> bool: ...


class BaseTaskManager:
    DEFAULT_TOPIC = 'tasks'
    callback_list: List[AbstractCallback]

    @classmethod
    @abc.abstractmethod
    async def create_subscription(
            cls,
            callback_list: List[AbstractCallback],
            topic: str = DEFAULT_TOPIC,
    ) -> ISubscriber: ...

    @classmethod
    @abc.abstractmethod
    async def create_publisher(
            cls,
            topic: str = DEFAULT_TOPIC,
    ) -> IPublisher: ...
