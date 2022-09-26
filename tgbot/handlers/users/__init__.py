from aiogram import Dispatcher

from tgbot.handlers.users.draw import register_user_draws
from tgbot.handlers.users.start import register_user_start_handlers


def register_user_handlers(dp: Dispatcher):
    register_user_start_handlers(dp)
    register_user_draws(dp)
