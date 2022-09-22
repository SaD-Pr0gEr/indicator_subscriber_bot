from aiogram import Dispatcher

from tgbot.filters.admin import register_admin_filters
from tgbot.filters.chat import register_chat_filters


def register_all_filters(dp: Dispatcher):
    register_admin_filters(dp)
    register_chat_filters(dp)
