import base64
import pickle
import uuid
from typing import Callable, Any

from queue.callbacks import AbstractCallback, AbstractCallbackResult, AbstractMessage
from queue.enums import MessageStatus


class PostgresMessage(AbstractMessage):

    async def to_dict(self):
        return self.__dict__

    async def serialize(self) -> Any:
        return base64.b64encode(pickle.dumps(self)).decode()

    @classmethod
    async def deserialize(cls, string: str):
        return pickle.loads(base64.b64decode(string))


class PostgresCallbackResult(AbstractCallbackResult):
    ...


class PostgresCallback(AbstractCallback):
    def __init__(
            self,
            idn: uuid.UUID,
            payload: dict,
            status: MessageStatus,
            callback: Callable = None
    ):
        self.idn = idn
        self.payload = payload
        self.status = status
        self.callback = callback

    async def fetch(self) -> PostgresCallbackResult:
        print(f"Callback: {id(self)}")
        return PostgresCallbackResult(
            result=PostgresMessage(
                idn=self.idn,
                payload=self.payload,
                status=self.status,
                callback=self.callback
            ),
        )
