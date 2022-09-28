import asyncio
import os
from datetime import datetime
from typing import Union

from aiogram import Bot
from aiogram.types import InputFile

from tgbot.config import Config, DRAW_MEMBERS_FILE_PATH
from tgbot.models.models import Draw, Users, DrawMember
from tgbot.services.excel import DrawMembersList


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


async def wait_draw_start(draw: Draw, sleep_time: Union[int, float], bot: Bot):
    await asyncio.sleep(sleep_time)
    check_draw: Draw = await Draw.query.where(
        Draw.Id == draw.Id
    ).gino.first()
    if check_draw.cancelled:
        return
    await check_draw.update(active=True).apply()
    for admin in bot["config"].tg_bot.admin_ids:
        await bot.send_photo(
            admin,
            photo=InputFile(draw.preview_photo_path),
            caption=f"Розыгрыш стартовал! Он завершится в {check_draw.end_date}"
        )
    users = await Users.query.gino.all()
    await draw_start(bot, users, draw)
    await wait_draw_end(
        draw,
        (draw.end_date - draw.start_date).total_seconds(),
        bot
    )


async def wait_draw_end(draw: Draw, sleep_time: Union[int, float], bot: Bot):
    await asyncio.sleep(sleep_time)
    check_draw: Draw = await Draw.query.where(
        Draw.Id == draw.Id
    ).gino.first()
    if check_draw.cancelled:
        return
    await check_draw.update(active=False).apply()
    members = await Users.join(DrawMember).select().where(
        DrawMember.draw == draw.Id
    ).gino.all()
    if not members:
        for admin in bot["config"].tg_bot.admin_ids:
            await bot.send_message(admin, "Участников нет, поэтому розыгрыш отменяется!")
        return
    manager = DrawMembersList(
        {"A1": "ID в телеграм", "B1": "@username в Telegram", "C1": "Номер телефона"}
    )
    file_path = f"{DRAW_MEMBERS_FILE_PATH / draw.name}.xlsx"
    manager.insert_data(members, file_path)
    for admin in bot["config"].tg_bot.admin_ids:
        await bot.send_photo(
            admin,
            InputFile(draw.preview_photo_path),
            f"Розыгрыш завершился! Пора провести стрим и разыграть призы!"
        )
        await bot.send_document(
            admin,
            InputFile(file_path),
            caption="Список участников. Пора устроить розыгрыш!"
        )
    os.remove(file_path)


async def draw_monitoring(bot: Bot, loop):
    draws = await Draw.query.where(Draw.cancelled == False).gino.all()
    if not draws:
        for admin in bot["config"].tg_bot.admin_ids:
            await bot.send_message(admin, "Мониторинг завершился... Розыгрышей нет")
        return
    task_list = []
    for draw in draws:
        if datetime.now() < draw.start_date:
            task = loop.create_task(wait_draw_start(
                draw,
                (draw.start_date - datetime.now()).total_seconds(),
                bot
            ))
            task_list.append(task)
        elif not draw.active or datetime.now() > draw.end_date:
            continue
        elif draw.start_date < datetime.now():
            task = loop.create_task(wait_draw_end(
                draw,
                (draw.end_date - datetime.now()).total_seconds(),
                bot
            ))
            task_list.append(task)
    for admin in bot["config"].tg_bot.admin_ids:
        if not task_list:
            await bot.send_message(admin, "Мониторинг завершился... Розыгрышей нет")
        else:
            await bot.send_message(
                admin,
                f"Мониторинг завершился... Найдены и активированы {len(task_list)} розыгрышы!"
            )
    if task_list:
        await asyncio.gather(*task_list)
