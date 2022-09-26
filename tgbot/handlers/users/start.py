from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from tgbot.data.commands import COMMANDS
from tgbot.filters.chat import PrivateChat
from tgbot.keyboards.reply import USER_SEND_NUMBER
from tgbot.misc.states import UserSignUp
from tgbot.models.models import Users
from tgbot.utils.keyboard import define_keyboard


async def user_start(message: Message):
    user = await Users.query.where(
        Users.tg_id == message.from_user.id
    ).gino.first()
    if not user:
        await UserSignUp.phone_number.set()
        await message.reply(
            "Привет! Чтобы подписаться отправьте мне свой номер телефона",
            reply_markup=USER_SEND_NUMBER
        )
        return
    await message.answer(
        "Привет! Выберите команду",
        reply_markup=define_keyboard(
            message.from_user.id, message.bot
        )
    )


async def get_user_number(message: Message, state: FSMContext):
    number = int(message.contact.phone_number.replace("+", ""))
    check_number = await Users.query.where(
        Users.phone_number == number
    ).gino.first()
    await state.finish()
    if check_number:
        await message.answer(
            "Пользователь с таким номером телефона уже существует!"
        )
        return
    await Users.create(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        phone_number=number
    )
    await message.answer(
        "Отлично! Вы успешно зарегистрировались!",
        reply_markup=define_keyboard(message.from_user.id, message.bot)
    )


async def call_command(message: Message):
    await message.bot.send_contact(
        message.from_user.id,
        "+998991501771",
        "Indicator UZ"
    )


def register_user_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_start, PrivateChat(),
        commands=["start"], state="*",
        commands_prefix="!/"
    )
    dp.register_message_handler(
        get_user_number, PrivateChat(),
        state=UserSignUp.phone_number,
        content_types=ContentType.CONTACT
    )
    dp.register_message_handler(
        call_command, PrivateChat(),
        text=COMMANDS["call_us"]
    )
