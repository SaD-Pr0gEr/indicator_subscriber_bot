import asyncio

from aiogram import Dispatcher
from aiogram.types import Message, InputFile

from tgbot.config import USERS_QR_CODE_SAVE_PATH
from tgbot.data.commands import COMMANDS
from tgbot.filters.chat import PrivateChat
from tgbot.models.models import Users
from tgbot.services.qr_code import QrGenerator


async def generate_users_qr_command(message: Message):
    user: Users = await Users.query.where(
        Users.tg_id == message.from_user.id
    ).gino.first()
    if not user:
        await message.answer("Вы не зарегистрированы!")
        return
    await message.answer("Отлично! Генерирую Qr...")
    await asyncio.sleep(2)
    bot = await message.bot.get_me()
    qr_path = QrGenerator(
        f"https://t.me/{bot.username}?start=user_personal_qr-{user.tg_id}",
        f"{USERS_QR_CODE_SAVE_PATH / str(user.Id)}.png"
    ).generate_and_save_qr()
    await user.update(qr_code_img_path=qr_path).apply()
    await message.bot.send_photo(
        message.from_user.id,
        InputFile(qr_path),
        caption=f"Ваш персональный QR код"
    )


async def my_qr(message: Message):
    user: Users = await Users.query.where(
        Users.tg_id == message.from_user.id
    ).gino.first()
    if not user:
        await message.answer("Вы не зарегистрированы!")
        return
    if not user.qr_code_img_path:
        await message.answer("У вас нет QR кода! Сначала генерируйте его")
        return
    await message.bot.send_photo(
        message.from_user.id,
        InputFile(user.qr_code_img_path),
        caption="Ваш личный QR код"
    )


def register_user_qr_handlers(dp: Dispatcher):
    dp.register_message_handler(
        generate_users_qr_command, PrivateChat(),
        text=COMMANDS["personal_qr"]
    )
    dp.register_message_handler(
        my_qr, PrivateChat(),
        text=COMMANDS["get_personal_qr"]
    )
