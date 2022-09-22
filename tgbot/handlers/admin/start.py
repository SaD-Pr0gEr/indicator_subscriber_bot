from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.data.commands import COMMANDS
from tgbot.filters.chat import PrivateChat
from tgbot.keyboards.reply import SUPERUSER_COMMANDS
from tgbot.models.models import Users


async def admin_start(message: Message):
    await message.reply(
        "Привет! Выберите команду",
        reply_markup=SUPERUSER_COMMANDS
    )


async def all_subscribers(message: Message):
    subs = await Users.query.gino.all()
    if not subs:
        await message.answer("Подписчиков нет)")
        return
    subs = '\n'.join(list(map(
        lambda model: f"@{model.username or model.tg_id}",
        subs
    )))
    await message.answer(f"Список подписчиков\n{subs}\nИтого: {len(subs)}")


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, PrivateChat(), commands=["start"],
        state="*", is_superuser=True, commands_prefix="!/"
    )
    dp.register_message_handler(
        all_subscribers, PrivateChat(),
        is_superuser=True, text=COMMANDS["subscribers_list"]
    )
