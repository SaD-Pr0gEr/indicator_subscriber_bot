import asyncio
from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tgbot.config import MAIN_DATE_FORMAT, DRAW_PHOTOS_DIR, HUMAN_READABLE_DATE_FORMAT
from tgbot.data.commands import COMMANDS
from tgbot.misc.states import AddDrawState, CancelDrawState
from tgbot.models.models import Draw, Users
from tgbot.utils.mailing import draw_start, draw_end, draw_cancelled


async def plan_draw_command(message: Message):
    await message.answer(
        "Отлично! Введите название розыгрыша"
    )
    await AddDrawState.name.set()


async def draw_title(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введите описание розыгрыша\n"
                         "Например, условия, призы и тп...")
    await AddDrawState.title.set()


async def draw_preview(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(
        "Отправьте фото розыгрыша(превью)"
    )
    await AddDrawState.photo.set()


async def draw_start_date(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer(
        f"Теперь введите дату начала в формате {HUMAN_READABLE_DATE_FORMAT}\n"
        f"Пример: 31.12.2022!01:59:55\n"
        f"Если хотите начать сразу то просто пишите *"
    )
    await AddDrawState.start_date.set()


async def draw_end_date(message: Message, state: FSMContext):
    date_text = datetime.now().strftime(MAIN_DATE_FORMAT) \
        if message.text == "*" else message.text.replace("!", " ")
    try:
        start_date = datetime.strptime(date_text, MAIN_DATE_FORMAT).strftime(MAIN_DATE_FORMAT)
        await state.update_data(start_date=start_date)
        await message.answer(
            f"Отлично! Теперь введите дату завершения "
            f"розыгрыша в формате {HUMAN_READABLE_DATE_FORMAT}\n"
            "Пример: 31.12.2022!01:59:55\n"
        )
        await AddDrawState.end_date.set()
    except ValueError:
        await message.answer(
            "Некорректный формат даты! Попробуйте ещё раз\n"
            "Пример: 27.10.2022!00:59:10"
        )


async def draw_winners(message: Message, state: FSMContext):
    date_text = message.text.replace("!", " ")
    try:
        end_date = datetime.strptime(date_text, MAIN_DATE_FORMAT).strftime(MAIN_DATE_FORMAT)
        await state.update_data(end_date=end_date)
        await message.answer("Теперь введите кол-во победителей в розыгрыше")
        await AddDrawState.winners_count.set()
    except ValueError:
        await message.answer(
            "Некорректный формат даты! Попробуйте ещё раз\n"
            "Пример: 27.10.2022!00:59:10"
        )


async def create_draw(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Вы ввели не число! Попробуйте ещё раз")
        return
    async with state.proxy() as data:
        name, title, photo_id, start_date, end_date = data.values()
    start_date = datetime.strptime(start_date, MAIN_DATE_FORMAT)
    end_date = datetime.strptime(end_date, MAIN_DATE_FORMAT)
    winners_count = int(message.text)
    await state.finish()
    photo = await message.bot.download_file_by_id(
        photo_id,
        destination_dir=DRAW_PHOTOS_DIR
    )
    users = await Users.query.gino.all()
    if end_date > start_date:
        draw = await Draw.create(
            name=name, title=title, preview_photo_path=photo.name,
            start_date=start_date, end_date=end_date, winners_count=winners_count
        )
        await message.answer(f"Розыгрыш активировался! Он завершится в {end_date}г.")
        await draw_start(message.bot, users, draw)
        await asyncio.sleep(abs((end_date - start_date).total_seconds()))
        check: Draw = await Draw.query.where(Draw.Id == draw.Id).gino.first()
        if check.cancelled:
            return
    else:
        draw = await Draw.create(
            name=name, title=title, preview_photo_path=photo.name,
            start_date=start_date, end_date=end_date, winners_count=winners_count,
            active=False
        )
        await message.answer(f"Розыгрыш активируется в {draw.start_date}г.!")
        await asyncio.sleep(abs((start_date - datetime.now()).total_seconds()))
        check: Draw = await Draw.query.where(Draw.Id == draw.Id).gino.first()
        if check.cancelled:
            return
        await draw_start(message.bot, users, draw)
        await message.answer(f"Розыгрыш активировался! Он завершится в {end_date}г.")
        await asyncio.sleep(abs((end_date - start_date).total_seconds()))
    await message.reply("Розыгрыш завершился! Пора провести стрим и разыграть призы!")
    await draw_end(message.bot, users, draw)


async def active_draws_list(message: Message):
    active_draws = await Draw.query.where(
        Draw.active == True
    ).gino.all()
    if not active_draws:
        await message.answer("Активных розыгрышей нет!")
        return
    active_draws = tuple(map(
        lambda model: f"ID: {model.Id}\n{model.name}\n"
                      f"Дата проведения: {model.start_date} - {model.end_date}\n"
                      f"Победители: {model.winners_count}",
        active_draws
    ))
    await message.answer(
        f"Активные розыгрышы:\n"
        f"{''.join(active_draws)}\n"
        f"Итого: {len(active_draws)}"
    )


async def all_draws(message: Message):
    draws_list = await Draw.query.gino.all()
    if not draws_list:
        await message.answer("Активных розыгрышей нет!")
        return
    draws_list = tuple(map(
        lambda model: f"ID: {model.Id}\n{model.name}\n"
                      f"Дата проведения: {model.start_date} - {model.end_date}\n"
                      f"Победители: {model.winners_count}\n\n",
        draws_list
    ))
    await message.answer(
        f"Все розыгрышы:\n"
        f"{''.join(draws_list)}\n"
        f"Итого: {len(draws_list)}"
    )


async def cancel_draw(message: Message):
    draws = await Draw.query.where(Draw.active == True).gino.all()
    if not draws:
        await message.answer("Активных розыгрышей нет!")
        return
    keyboard = InlineKeyboardMarkup()
    for draw in draws:
        keyboard.add(InlineKeyboardButton(draw.Id, callback_data=draw.Id))
    await CancelDrawState.draw.set()
    await message.answer(
        "Отлично! Выберите его Id из списка",
        reply_markup=keyboard
    )


async def cancel_draw_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(draw=int(callback.data))
    await CancelDrawState.confirm.set()
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Да", callback_data="yes")
    ).add(
        InlineKeyboardButton("Нет", callback_data="no")
    )
    await callback.bot.send_message(
        callback.from_user.id,
        "Вы уверены, что хотите отменить розыгрыш?",
        reply_markup=keyboard
    )


async def cancel_draw_confirm_callback(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        draw = data["draw"]
    await state.finish()
    match callback.data:
        case "yes":
            draw = await Draw.query.where(
                Draw.Id == draw
            ).gino.first()
            await draw.update(cancelled=True, active=False).apply()
            await draw_cancelled(
                callback.bot,
                await Users.query.gino.all()
            )
        case "no":
            await callback.bot.send_message(
                callback.from_user.id,
                "Команда отменена!"
            )
    await callback.bot.delete_message(
        callback.from_user.id,
        callback.message.message_id
    )


def register_draw_handlers(dp: Dispatcher):
    dp.register_message_handler(
        plan_draw_command, text=COMMANDS["add_draw"],
        is_superuser=True
    )
    dp.register_message_handler(
        draw_title, state=AddDrawState.name,
        is_superuser=True
    )
    dp.register_message_handler(
        draw_preview, state=AddDrawState.title,
        is_superuser=True
    )
    dp.register_message_handler(
        draw_start_date, state=AddDrawState.photo,
        content_types=[ContentType.PHOTO],
        is_superuser=True
    )
    dp.register_message_handler(
        draw_end_date, state=AddDrawState.start_date,
        is_superuser=True
    )
    dp.register_message_handler(
        draw_winners, state=AddDrawState.end_date,
        is_superuser=True
    )
    dp.register_message_handler(
        create_draw, state=AddDrawState.winners_count,
        is_superuser=True
    )
    dp.register_message_handler(
        active_draws_list, text=COMMANDS["active_draws"],
        is_superuser=True
    )
    dp.register_message_handler(
        all_draws, text=COMMANDS["all_draws"],
        is_superuser=True
    )
    dp.register_message_handler(
        cancel_draw, text=COMMANDS["cancel_draw"],
        is_superuser=True
    )
    dp.register_callback_query_handler(
        cancel_draw_callback, state=CancelDrawState.draw
    )
    dp.register_callback_query_handler(
        cancel_draw_confirm_callback, state=CancelDrawState.confirm
    )
