from tgbot.handlers.admin import register_admin_handlers
from tgbot.handlers.users import register_user_handlers
from tgbot.handlers.users.qr import register_user_qr_handlers


def register_all_handlers(dp):
    register_admin_handlers(dp)
    register_user_handlers(dp)
    register_user_qr_handlers(dp)
