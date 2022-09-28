from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tgbot.data.commands import COMMANDS
from tgbot.filters.chat import PrivateChat
from tgbot.misc.states import AddAdminState, DeleteAdminState
from tgbot.models.models import Users


async def admins_list(message: Message):
    admins = await Users.query.where(
        Users.is_admin == True
    ).gino.all()
    if not admins:
        await message.answer("Админов пока нет)")
        return
    admins = '\n'.join(list(map(
        lambda model: f"👤 @{model.username}" or f"👤 +{model.phone_number}",
        admins
    )))
    await message.answer(f"Список админов\n{admins}")


async def add_admin_command(message: Message):
    await message.answer("Отлично! Введите его telegram ID\n"
                         "ВНИМАНИЯ!!! Он должен быть зарегистрированным пользователем!")
    await AddAdminState.tg_id.set()


async def get_user_id_and_add_admin(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите числа, а не буквы!")
        return
    await state.finish()
    user = await Users.query.where(
        Users.tg_id == int(message.text)
    ).gino.first()
    if not user:
        await message.answer("Пользователь не найден! Попробуйте заново")
        return
    await user.update(is_admin=True).apply()
    await message.answer("Админ успешно добавлен!")


async def delete_admin_command(message: Message):
    keyboard = InlineKeyboardMarkup()
    admins = await Users.query.where(
        Users.is_admin == True
    ).gino.all()
    if not admins:
        await message.answer("Админов пока нет")
        return
    for i in admins:
        keyboard.add(InlineKeyboardButton(
            f"{'@' + i.username or f'+{i.phone_number}'}",
            callback_data=f"{i.tg_id}"
        ))
    await DeleteAdminState.callback_state.set()
    await message.answer(
        "Отлично! Выберите админа из списка",
        reply_markup=keyboard
    )


async def delete_admin_callback(callback: CallbackQuery, state: FSMContext):
    admin: Users = await Users.query.where(
        Users.tg_id == int(callback.data)
    ).gino.first()
    await admin.update(is_admin=False).apply()
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    await callback.bot.send_message(
        callback.from_user.id,
        "Успешно понизил!"
    )
    await state.finish()


def register_admins_crud_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admins_list, PrivateChat(),
        is_superuser=True, text=COMMANDS["admins_list"]
    )
    dp.register_message_handler(
        add_admin_command, PrivateChat(),
        is_superuser=True, text=COMMANDS["add_admin"]
    )
    dp.register_message_handler(
        get_user_id_and_add_admin, PrivateChat(),
        is_superuser=True, state=AddAdminState.tg_id
    )
    dp.register_message_handler(
        delete_admin_command, PrivateChat(),
        is_superuser=True, text=COMMANDS["kick_admin"]
    )
    dp.register_callback_query_handler(
        delete_admin_callback, is_superuser=True,
        state=DeleteAdminState.callback_state
    )
