from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from tgbot.config import BASE_DIR
from tgbot.data.commands import COMMANDS
from tgbot.misc.states import AddDrawState
from tgbot.models.models import Draw
from tgbot.utils.datetime_utils import sleep_and_activate_draw, sleep_and_deactivate_draw


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
        "Теперь введите дату начала в формате дд.мм.ГГГГ!часы:минуты:секунды\n"
        "Пример: 31.12.2022!01:59:55\n"
        "Если хотите начать сразу то просто пишите *"
    )
    await AddDrawState.start_date.set()


async def draw_end_date(message: Message, state: FSMContext):
    date_text = datetime.now().strftime("%d.%m.%Y %H:%M:%S") \
        if message.text == "*" else message.text.replace("!", " ")
    try:
        start_date = datetime.strptime(date_text, "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%Y %H:%M:%S")
        await state.update_data(start_date=start_date)
        await message.answer(
            "Отлично! Теперь введите дату завершения розыгрыша в формате дд.мм.ГГГГ!часы:минуты:секунды\n"
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
        end_date = datetime.strptime(date_text, "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%Y %H:%M:%S")
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
    winners_count = int(message.text)
    async with state.proxy() as data:
        name, title, photo_id, start_date, end_date = data.values()
    await state.finish()
    photo_dir = BASE_DIR / "photos/draw"
    photo = await message.bot.download_file_by_id(
        photo_id,
        destination=photo_dir
    )
    start_date = datetime.strptime(start_date, "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(end_date, "%d.%m.%Y %H:%M:%S")
    if datetime.now() > start_date:
        draw = await Draw.create(
            name=name, title=title, preview_photo_path=photo.name,
            start_date=start_date, end_date=end_date, winners_count=winners_count
        )
        await sleep_and_deactivate_draw(
            draw, abs((datetime.now() - start_date).total_seconds())
        )
    else:
        draw = await Draw.create(
            name=name, title=title, preview_photo_path=photo.name,
            start_date=start_date, end_date=end_date, winners_count=winners_count,
            active=False
        )
        await message.answer(f"Розыгрыш активируется в {draw.start_date}г.!")
        await sleep_and_activate_draw(
            draw, abs((start_date - datetime.now()).total_seconds())
        )
        await sleep_and_deactivate_draw(
            draw, abs((start_date - end_date).total_seconds())
        )
        await message.answer(f"Розыгрыш активировался! Он завершится в {end_date}г.")


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
