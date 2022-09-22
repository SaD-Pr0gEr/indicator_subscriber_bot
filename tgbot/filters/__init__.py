from aiogram import Dispatcher

from tgbot.filters.admin import register_admin_filters


def register_all_filters(dp: Dispatcher):
    register_admin_filters(dp)
