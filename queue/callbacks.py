import abc
import uuid
from dataclasses import dataclass
from typing import Optional, Any

from queue.enums import MessageStatus


@dataclass
class AbstractMessage:
    idn: uuid.UUID
    payload: dict
    status: MessageStatus
    callback: Optional["AbstractCallback"]

    @abc.abstractmethod
    async def serialize(self) -> Any: ...


@dataclass
class AbstractCallbackResult:
    result: "AbstractMessage"


class AbstractCallback(abc.ABC):
    @abc.abstractmethod
    async def fetch(self) -> AbstractCallbackResult: ...
