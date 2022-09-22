from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
