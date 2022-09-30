from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from tgbot.data.commands import COMMANDS
from tgbot.data.general import BONUSES
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
        if "R" in message.text:
            referrer_id = int(message.text.split("R")[-1])
            referrer: Users = await Users.query.where(
                Users.tg_id == referrer_id
            ).gino.first()
            if referrer:
                referrer_bonus = BONUSES["referrer_bonus"]
                await referrer.update(
                    balance=referrer.balance + referrer_bonus
                ).apply()
                await message.bot.send_message(
                    referrer.tg_id,
                    f"Вам начислено {referrer_bonus} баллов как реферальный бонус!"
                )
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
        phone_number=number,
        balance=50, subscribed_date=datetime.now().date()
    )
    await message.answer(
        "Отлично! Вы успешно зарегистрировались!\nВам начислено 50 баллов для старта!",
        reply_markup=define_keyboard(message.from_user.id, message.bot)
    )


async def call_command(message: Message):
    await message.bot.send_contact(
        message.from_user.id,
        "+998991501771",
        "Indicator UZ"
    )


async def get_referral_link_command(message: Message):
    bot = await message.bot.get_me()
    await message.answer(
        f"Ваша реферальная ссылка\bhttps://t.me/{bot.username}?start=R{message.from_user.id}"
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
    dp.register_message_handler(
        get_referral_link_command, PrivateChat(),
        text=COMMANDS["my_referral_link"]
    )
