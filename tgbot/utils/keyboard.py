from aiogram import Bot

from tgbot.keyboards.reply import (
    SUPERUSER_COMMANDS,
    ADMIN_COMMANDS,
    USER_COMMANDS
)


def define_keyboard(user_id: int, bot: Bot, admin_ids: list = None):
    if user_id in bot["config"].tg_bot.admin_ids:
        return SUPERUSER_COMMANDS
    elif admin_ids and user_id in admin_ids:
        return ADMIN_COMMANDS
    return USER_COMMANDS
