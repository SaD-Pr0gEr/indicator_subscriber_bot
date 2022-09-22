from aiogram import Dispatcher

from tgbot.handlers.admin.admin_crud import register_admins_crud_handlers
from tgbot.handlers.admin.start import register_start_handlers


def register_admin_handlers(dp: Dispatcher):
    register_start_handlers(dp)
    register_admins_crud_handlers(dp)