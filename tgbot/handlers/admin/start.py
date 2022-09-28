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
    subs_db: list[Users] = await Users.query.gino.all()
    if not subs_db:
        await message.answer("Подписчиков нет)")
        return
    text = "\n".join(map(
        lambda model: f"👤 @{model.username}\n"
                      f"💰 Баланс: {model.balance}\n"
                      f'📅 Дата регистрации: {model.subscribed_date}\n'
        if model.username else
        f"👤 +{model.phone_number}\n"
        f"💰 Баланс: {model.balance}\n"
        f"📅 Дата регистрации: {model.subscribed_date}\n",
        subs_db
    ))
    await message.answer(f"Список подписчиков\n\n{text}\n\nИтого: {len(subs_db)} шт.")


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, PrivateChat(), commands=["start"],
        state="*", is_superuser=True, commands_prefix="!/"
    )
    dp.register_message_handler(
        all_subscribers, PrivateChat(),
        is_superuser=True, text=COMMANDS["subscribers_list"]
    )
