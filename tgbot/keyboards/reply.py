from aiogram.types import ReplyKeyboardMarkup

from tgbot.buttons.reply import (
    ADD_ADMIN, SUBSCRIBERS_LIST,
    ADMINS_LIST, KICK_ADMIN,
    CALL_US, SEND_NUMBER, ADD_POST,
    ADD_DRAW, ALL_DRAWS, ACTIVE_DRAWS,
    CANCEL_DRAW
)

SUPERUSER_COMMANDS = ReplyKeyboardMarkup([
    [ADD_ADMIN, SUBSCRIBERS_LIST],
    [ADMINS_LIST, KICK_ADMIN],
    [ADD_POST, ADD_DRAW],
    [ALL_DRAWS, ACTIVE_DRAWS],
    [CANCEL_DRAW],
], resize_keyboard=True)


ADMIN_COMMANDS = ReplyKeyboardMarkup([
    [SUBSCRIBERS_LIST, ADD_POST],
], resize_keyboard=True)


USER_COMMANDS = ReplyKeyboardMarkup([
    [CALL_US]
], resize_keyboard=True)


USER_SEND_NUMBER = ReplyKeyboardMarkup([
    [SEND_NUMBER]
], resize_keyboard=True)
