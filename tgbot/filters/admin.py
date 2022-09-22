import typing

from aiogram import Dispatcher
from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config


class SuperuserFilter(BoundFilter):
    key = 'is_superuser'

    def __init__(self, is_superuser: typing.Optional[bool] = None):
        self.is_superuser = is_superuser

    async def check(self, obj):
        if self.is_superuser is None:
            return False
        config: Config = obj.bot.get('config')
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_superuser


def register_admin_filters(dp: Dispatcher):
    dp.filters_factory.bind(SuperuserFilter)
