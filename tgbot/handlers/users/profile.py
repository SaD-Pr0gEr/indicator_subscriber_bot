from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.data.commands import COMMANDS
from tgbot.filters.chat import PrivateChat
from tgbot.models.models import Users


async def user_balance(message: Message):
    user: Users = await Users.query.where(
        Users.tg_id == message.from_user.id
    ).gino.first()
    if not user:
        await message.answer("Вы не подписаны")
        return
    await message.answer(f"💸 Ваш баланс:\n{user.balance} балл")


def register_user_profile_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_balance, PrivateChat(),
        text=COMMANDS["balance"]
    )
