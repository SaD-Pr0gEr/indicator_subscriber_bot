import os

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile, ContentType

from tgbot.config import BASE_DIR
from tgbot.data.commands import COMMANDS
from tgbot.filters.chat import PrivateChat
from tgbot.filters.users import StaffFilter
from tgbot.misc.states import PostPublishState
from tgbot.models.models import Users


async def create_news_command(message: Message):
    await message.answer("Отлично! Введите название поста")
    await PostPublishState.post_name.set()


async def get_post_name(message: Message, state: FSMContext):
    await state.update_data(post_name=message.text)
    await PostPublishState.post_title.set()
    await message.answer(
        "Отлично! Теперь введите содержимое поста"
    )


async def get_post_title(message: Message, state: FSMContext):
    await state.update_data(post_title=message.text)
    await PostPublishState.post_preview.set()
    await message.answer(
        "Теперь отправьте фото для поста"
    )


async def get_post_preview(message: Message, state: FSMContext):
    async with state.proxy() as data:
        post_name = data["post_name"]
        post_title = data["post_title"]
    photo_id = message.photo[-1].file_id
    photos_dir = BASE_DIR / "photos/news"
    filename = await message.bot.download_file_by_id(
        photo_id,
        destination_dir=photos_dir
    )
    await state.finish()
    await message.answer("Отправляю всем...")
    for user in await Users.query.gino.all():
        await message.bot.send_photo(
            user.tg_id,
            photo=InputFile(filename.name),
            caption=f"<b>{post_name}</b>\n\t\t\t\t{post_title}",
        )
    await message.answer("Отлично! Пост отправлен всем подписчикам!")
    if os.path.exists(filename.name):
        os.remove(filename.name)


def register_news_handlers(dp: Dispatcher):
    dp.register_message_handler(
        create_news_command, PrivateChat(),
        StaffFilter(), text=COMMANDS["add_news"]
    )
    dp.register_message_handler(
        get_post_name, PrivateChat(),
        state=PostPublishState.post_name
    )
    dp.register_message_handler(
        get_post_title, PrivateChat(),
        state=PostPublishState.post_title
    )
    dp.register_message_handler(
        get_post_preview, PrivateChat(),
        state=PostPublishState.post_preview,
        content_types=[ContentType.PHOTO]
    )
