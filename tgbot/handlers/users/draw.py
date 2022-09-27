from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from sqlalchemy import and_

from tgbot.data.commands import COMMANDS
from tgbot.filters.chat import PrivateChat
from tgbot.misc.states import ParticipateDrawState
from tgbot.models.models import Draw, Users, DrawMember, db


async def draws_list(message: Message):
    async with db.transaction():
        cursor = await Draw.query.where(
            Draw.active == True
        ).gino.iterate()
        draws = await cursor.many(2)
    if not draws:
        await message.answer("Активных розыгрышев пока нет")
        return
    keyboard = InlineKeyboardMarkup()
    send_draw = draws[0]
    if len(draws) > 1:
        keyboard.add(InlineKeyboardButton(
            "Следующий >>",
            callback_data=f"!{1}"
        ))
    await ParticipateDrawState.choose_draw.set()
    keyboard.add(
        InlineKeyboardButton(
            "Учавствовать!",
            callback_data=f"{send_draw.Id}:{message.from_user.id}"
        ),
        InlineKeyboardButton(
            "Отмена ❌",
            callback_data="cancel"
        )
    )
    await message.bot.send_photo(
        message.from_user.id,
        InputFile(send_draw.preview_photo_path),
        caption=f"{send_draw.name}\n{send_draw.title}\n"
                f"Победители: {send_draw.winners_count}\n"
                f"Даты проведения: {send_draw.start_date} - {send_draw.end_date}",
        reply_markup=keyboard
    )


async def choose_draw(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    if "!" in callback.data:
        skip_count = int(callback.data.split("!")[-1])
        async with db.transaction():
            cursor = await Draw.query.where(
                Draw.active == True
            ).gino.iterate()
            if skip_count > 0:
                await cursor.forward(skip_count)
            draws = await cursor.many(2)
        send_draw = draws[0]
        if len(draws) > 1:
            keyboard.add(InlineKeyboardButton(
                ">> Следующий",
                callback_data=f"!{skip_count + 1}"
            ))
        keyboard.add(InlineKeyboardButton(
            "<< Предыдущий", callback_data=f"!{skip_count - 1}")
        ) if skip_count - 1 >= 0 else None
        keyboard.add(
            InlineKeyboardButton(
                "Учавствовать!",
                callback_data=f"{send_draw.Id}:{callback.from_user.id}"
            ),
            InlineKeyboardButton(
                "Отмена ❌",
                callback_data="cancel"
            )
        )
        await callback.bot.delete_message(
            callback.from_user.id,
            callback.message.message_id
        )
        await callback.bot.send_photo(
            callback.from_user.id,
            InputFile(send_draw.preview_photo_path),
            caption=f"{send_draw.name}\n{send_draw.title}\n"
                    f"Победители: {send_draw.winners_count}\n"
                    f"Даты проведения: {send_draw.start_date} - {send_draw.end_date}",
            reply_markup=keyboard
        )
    elif ":" in callback.data:
        raw_data = callback.data.split(":")
        draw_id, user_id = tuple(map(
            int, raw_data
        ))
        check_user = await Users.query.where(
            Users.tg_id == user_id
        ).gino.first()
        if not check_user:
            await callback.bot.send_message(
                callback.from_user.id,
                "Вы не зарегистрированы!"
            )
            await state.finish()
            await callback.bot.delete_message(
                callback.from_user.id,
                callback.message.message_id
            )
            return
        draw = await Draw.query.where(and_(
            Draw.Id == draw_id,
            Draw.active == True
        )).gino.first()
        if not draw:
            await callback.bot.send_message(
                callback.from_user.id,
                "Розыргыш уже завершился!"
            )
            return
        if await DrawMember.query.where(
                DrawMember.member == check_user.Id,
        ).gino.first():
            await callback.bot.send_message(
                callback.from_user.id,
                "Вы и так учавствуете!"
            )
            return
        await DrawMember.create(
            member=check_user.Id,
            draw=draw.Id
        )
        await callback.bot.send_message(
            callback.from_user.id,
            "Отлично! Вы учавствуете в розыгрыше!"
        )
    else:
        await state.finish()
        await callback.bot.delete_message(
            callback.from_user.id,
            callback.message.message_id
        )


def register_user_draws(dp: Dispatcher):
    dp.register_message_handler(
        draws_list, PrivateChat(),
        text=COMMANDS["active_draws"]
    )
    dp.register_callback_query_handler(
        choose_draw, state=ParticipateDrawState.choose_draw
    )
