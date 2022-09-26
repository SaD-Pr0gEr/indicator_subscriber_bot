from typing import Union

from aiogram import Bot
from aiogram.types import InputFile

from tgbot.models.models import Draw, Users, DrawMember


async def draw_start(bot: Bot, users_list: Union[list[Users], tuple[Users]], draw: Draw) -> None:
    for user in users_list:
        await bot.send_photo(
            user.tg_id,
            InputFile(draw.preview_photo_path),
            caption=f"<b>Внимание розыгрыш❗❗❗</b>\n"
                    f"{draw.name}\n{draw.title}\n"
                    f"Кол-во победителей: {draw.winners_count}\n"
                    f"Дата проведения: с {draw.start_date} по {draw.end_date}\n"
                    f"Розыгрыш проведётся в прямом эфире на нашем телеграм канале!\n"
                    f"Так что не пропусти стрим и выиграй ценные призы!\n"
                    f"Лови ссылку на наш канал)\n<a href='https://t.me/vollex_frontend'>"
                    f"Наш канал</a>"
        )


async def draw_end(bot: Bot, users_list: Union[list[Users], tuple[Users]], draw: Draw) -> None:
    for user in users_list:
        await bot.send_photo(
            user.tg_id,
            InputFile(draw.preview_photo_path),
            caption=f"Розыгрыш завершился! Прямо сейчас на стриме "
                    f"выбираем {draw.winners_count} победителей!\n"
                    f"Так что не пропусти стрим и выиграй ценные призы!\n"
                    f"Лови ссылку на наш канал)\n<a href='https://t.me/vollex_frontend'>"
                    f"Наш канал</a>"
        )


async def draw_cancelled(bot: Bot, users_list: Union[list[Users], tuple[Users]]):
    for user in users_list:
        await bot.send_message(
            user.tg_id,
            "ВНИМАНИЕ❗❗❗\nРозыргыш отменяется админом!\n"
            "Приносим свои извенения за предоставленное неудобство("
        )
