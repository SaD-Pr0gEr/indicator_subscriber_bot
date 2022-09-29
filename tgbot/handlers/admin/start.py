from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tgbot.data.commands import COMMANDS
from tgbot.data.general import BONUSES
from tgbot.filters.chat import PrivateChat
from tgbot.filters.users import StaffFilter
from tgbot.keyboards.reply import STAFF_CHOOSE_BONUS
from tgbot.misc.states import UserBonusesState
from tgbot.models.models import Users
from tgbot.utils.keyboard import define_keyboard


async def admin_start(message: Message):
    if "user_personal_qr" in message.text:
        user_id = int(message.text.split("-")[-1])
        user: Users = await Users.query.where(
            Users.tg_id == user_id
        ).gino.first()
        if not user:
            await message.answer("Пользователь не найден!")
            return
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(
            "Начислить бонус 🤑",
            callback_data=f"bonus:{user.tg_id}")
        )
        await message.answer(
            f"Пользователь найден!\n"
            f"👤 {f'@{user.username}' or f'+{user.phone_number}'}\n"
            f"🆔 {user.tg_id}",
            reply_markup=keyboard
        )
        await UserBonusesState.choose_command.set()
    else:
        keyboard = define_keyboard(message.from_user.id, message.bot)
        await message.reply(
            "Привет! Выберите команду",
            reply_markup=keyboard
        )


async def admin_user_option_callback(callback: CallbackQuery, state: FSMContext):
    if "bonus" in callback.data:
        user_id = int(callback.data.split(":")[-1])
        await state.update_data(choose_command=user_id)
        await UserBonusesState.choose_bonus_type.set()
        await callback.bot.send_message(
            callback.from_user.id,
            "Отлично! Выберите тип бонуса",
            reply_markup=STAFF_CHOOSE_BONUS
        )


async def define_user_bonus(message: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data["choose_command"]
    user: Users = await Users.query.where(
        Users.tg_id == user_id
    ).gino.first()
    if message.text not in BONUSES.keys():
        await UserBonusesState.personal_bonus.set()
        await message.answer("Отлично! Введите сколько хотите начислить")
        return
    balance = user.balance + BONUSES[message.text]
    await user.update(balance=balance).apply()
    await state.finish()
    await message.answer(
        "Успешно начислил!",
        reply_markup=define_keyboard(
            message.from_user.id,
            message.bot
        )
    )
    await message.bot.send_message(
        user.tg_id,
        f"Вам начислено {BONUSES[message.text]} баллов в качестве бонуса!\n"
        f"Ваш баланс: {user.balance}"
    )


async def personal_bonus(message: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data["choose_command"]
    user = await Users.query.where(
        Users.tg_id == user_id
    ).gino.first()
    balance = int(message.text) + user.balance
    await user.update(balance=balance).apply()
    await message.answer(
        "Успешно начислил!",
        reply_markup=define_keyboard(
            message.from_user.id,
            message.bot
        )
    )
    await message.bot.send_message(
        user.tg_id,
        f"Вам начислено {int(message.text)} баллов!\n"
        f"Ващ текущий баланс: {user.balance}"
    )
    await state.finish()


async def all_subscribers(message: Message):
    subs_db: list[Users] = await Users.query.gino.all()
    if not subs_db:
        await message.answer("Подписчиков нет)")
        return
    text = "\n".join(map(
        lambda model: f"👤 @{model.username}\n"
                      f"🆔 Telegram Id: {model.tg_id}\n"
                      f"💰 Баланс: {model.balance}\n"
                      f'📅 Дата регистрации: {model.subscribed_date}\n'
        if model.username else
        f"👤 +{model.phone_number}\n"
        f"🆔 Telegram Id: {model.tg_id}\n"
        f"💰 Баланс: {model.balance}\n"
        f"📅 Дата регистрации: {model.subscribed_date}\n",
        subs_db
    ))
    await message.answer(f"Список подписчиков\n\n{text}\n\nИтого: {len(subs_db)} шт.")


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, PrivateChat(),
        StaffFilter(), commands=["start"],
        state="*", commands_prefix="!/"
    )
    dp.register_message_handler(
        all_subscribers, PrivateChat(),
        StaffFilter(), text=COMMANDS["subscribers_list"]
    )
    dp.register_callback_query_handler(
        admin_user_option_callback, state=UserBonusesState.choose_command
    )
    dp.register_message_handler(
        define_user_bonus, StaffFilter(),
        state=UserBonusesState.choose_bonus_type,
    )
    dp.register_message_handler(
        personal_bonus, StaffFilter(),
        state=UserBonusesState.personal_bonus
    )
