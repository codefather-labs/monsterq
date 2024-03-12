import asyncio
import uuid
from typing import List

from pubsub import TaskManager, Subscriber, Publisher
from queue.backends.callbacks import PostgresCallback
from queue.backends.postgres import PostgresMessage
from queue.enums import MessageStatus

loop = asyncio.get_event_loop()
TaskManager.set_event_loop(loop)

callback_list = [
    PostgresCallback(
        idn=uuid.uuid4(),
        payload={"test": 1},
        status=MessageStatus.INITED,
        callback=None
    ),
    PostgresCallback(
        idn=uuid.uuid4(),
        payload={"test": 2},
        status=MessageStatus.INITED,
        callback=None
    ),
    PostgresCallback(
        idn=uuid.uuid4(),
        payload={"test": 3},
        status=MessageStatus.INITED,
        callback=None
    )
]


async def main(callback_list: List[PostgresCallback]):
    subscriber: Subscriber = await TaskManager.create_subscription(callback_list=callback_list)
    publisher: Publisher = await TaskManager.create_publisher()

    print(subscriber, publisher)
    await asyncio.sleep(1)

    await publisher.push(message=PostgresMessage(
        idn=uuid.uuid4(),
        payload={},
        status=MessageStatus.INITED,
        callback=None
    ))

    await asyncio.sleep(3)
    print(subscriber.connection.is_alive)
    await subscriber.close()
    print(subscriber.connection.is_alive)

    print("---")
    print(publisher.connection.is_alive)
    await publisher.close()
    print(publisher.connection.is_alive)


loop.run_until_complete(main(callback_list))
