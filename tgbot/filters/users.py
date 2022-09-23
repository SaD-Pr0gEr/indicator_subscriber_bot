from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from tgbot.models.models import Users


class StaffFilter(BoundFilter):

    async def check(self, message: Message) -> bool:
        opt_1 = message.from_user.id in message.bot["config"].tg_bot.admin_ids
        opt_2 = await Users.query.where(
            Users.tg_id == message.from_user.id
        ).gino.first()
        return opt_1 or opt_2
