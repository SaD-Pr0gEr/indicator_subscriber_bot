from aiogram.types import ReplyKeyboardMarkup

from tgbot.buttons.reply import (
    ADD_ADMIN, SUBSCRIBERS_LIST,
    ADMINS_LIST, KICK_ADMIN,
    CALL_US, SEND_NUMBER
)

SUPERUSER_COMMANDS = ReplyKeyboardMarkup([
    [ADD_ADMIN, SUBSCRIBERS_LIST],
    [ADMINS_LIST, KICK_ADMIN],
], resize_keyboard=True)


ADMIN_COMMANDS = ReplyKeyboardMarkup([
    [SUBSCRIBERS_LIST],
], resize_keyboard=True)


USER_COMMANDS = ReplyKeyboardMarkup([
    [CALL_US]
], resize_keyboard=True)


USER_SEND_NUMBER = ReplyKeyboardMarkup([
    [SEND_NUMBER]
], resize_keyboard=True)
