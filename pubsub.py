import asyncio
from asyncio import AbstractEventLoop
from typing import List, Optional

from interfaces import BaseTaskManager, ISubscriber, IPublisher, ISubscriberEventCallback
from queue.backends.callbacks import PostgresCallback
from queue.backends.postgres import PostgresBackend, PostgresMessage


class TaskManager(BaseTaskManager, PostgresBackend):
    loop: Optional[AbstractEventLoop] = None

    @staticmethod
    def set_event_loop(loop: AbstractEventLoop):
        TaskManager.loop = loop
        PostgresBackend.loop = loop

    async def wait_for_connection(self):
        while not self.connection or not self.connection.is_alive:
            await asyncio.sleep(0.1)

    @classmethod
    async def create_subscription(
            cls,
            callback_list: List[PostgresCallback],
            topic: str = BaseTaskManager.DEFAULT_TOPIC,
    ) -> "Subscriber":
        sub = Subscriber()
        await sub.create_connection()
        await sub.wait_for_connection()

        await sub.set_subscription_callback_list(
            topic=topic,
            callback_list=callback_list,
        )
        return sub

    @classmethod
    async def create_publisher(
            cls,
            topic: str = BaseTaskManager.DEFAULT_TOPIC
    ) -> "Publisher":
        pub = Publisher()
        await pub.wait_for_connection()
        # TODO
        # await pub.set_publisher_topic
        return pub


class SubscriberEventCallback(ISubscriberEventCallback):
    callback_list: List[PostgresCallback]

    async def on_event_callback(self, *args, **kwargs):
        # TODO callback message impl
        # TODO шото непонятное происходит. на входит приходит 3 коллбека из теста
        # TODO а сюда приходит один, с ни один айдишник со входным не совпадает
        # возможно я туплю

        topic = args[2]  # todo message.topic
        message: PostgresMessage = await PostgresMessage.deserialize(args[3])

        # [await cb.fetch() for cb in self.callback_list]
        # l = [cb(**await msg.to_dict()) for cb in self.callback_list]
        # print(l)
        print(f"--- subscriber callback")
        print(message)
        print(f"--- subscriber callback done")
        return


class Subscriber(ISubscriber, SubscriberEventCallback, TaskManager):
    async def pop(self) -> PostgresMessage:
        # TODO impl

        # TODO
        message: PostgresMessage = await self.get_last_pending()
        print(message)
        print(self)

        return message

    async def set_subscription_callback_list(
            self,
            topic: str,
            callback_list: List[PostgresCallback],
    ):
        self.callback_list = callback_list
        await self.connection.add_listener(topic, self.on_event_callback)

    @property
    def is_alive(self):
        return not self.connection.is_alive if self.connection else False

    async def close(self):
        await self.connection.close()


class Publisher(IPublisher, TaskManager):

    async def push(self, message: PostgresMessage) -> bool:
        print(message)
        print(self)
        # TODO
        await self.send_message(message)

        return True

    @property
    def is_alive(self):
        return not self.connection.is_alive if self.connection else False

    async def close(self):
        await self.connection.close()
