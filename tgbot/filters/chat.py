from aiogram import Dispatcher
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, ChatType


class PrivateChat(BoundFilter):

    async def check(self, message: Message) -> bool:
        return message.chat.type == ChatType.PRIVATE


class PublicChat(BoundFilter):

    async def check(self, message: Message) -> bool:
        return message.chat.type == ChatType.GROUP \
               or message.chat.type == ChatType.SUPERGROUP


def register_chat_filters(dp: Dispatcher):
    dp.filters_factory.bind(PublicChat)
    dp.filters_factory.bind(PrivateChat)
