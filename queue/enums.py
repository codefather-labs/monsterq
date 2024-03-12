from enum import Enum


class MessageStatus(Enum):
    INITED = 'inited'
    CREATED = 'created'
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
