from aiogram.types import ReplyKeyboardMarkup

from tgbot.buttons.reply import (
    ADD_ADMIN, SUBSCRIBERS_LIST,
    ADMINS_LIST, KICK_ADMIN,
    CALL_US, SEND_NUMBER, ADD_POST,
    ADD_DRAW, ALL_DRAWS, ACTIVE_DRAWS,
    CANCEL_DRAW, DRAW_MEMBERS, BALANCE,
    PERSONAL_QR_CODE, GET_PERSONAL_QR,
    BOUGHT_BONUS, SERVICE_BONUS,
    PERSONAL_BONUS, REFERRAL_LINK
)

SUPERUSER_COMMANDS = ReplyKeyboardMarkup([
    [ADD_ADMIN, SUBSCRIBERS_LIST],
    [ADMINS_LIST, KICK_ADMIN],
    [ADD_POST, ADD_DRAW],
    [ALL_DRAWS, ACTIVE_DRAWS],
    [CANCEL_DRAW, DRAW_MEMBERS],
], resize_keyboard=True)


ADMIN_COMMANDS = ReplyKeyboardMarkup([
    [SUBSCRIBERS_LIST, ADD_POST],
    [DRAW_MEMBERS, ACTIVE_DRAWS],
    [ALL_DRAWS]
], resize_keyboard=True)


USER_COMMANDS = ReplyKeyboardMarkup([
    [CALL_US, ACTIVE_DRAWS],
    [BALANCE, PERSONAL_QR_CODE],
    [GET_PERSONAL_QR, REFERRAL_LINK]
], resize_keyboard=True)


STAFF_CHOOSE_BONUS = ReplyKeyboardMarkup([
    [BOUGHT_BONUS, SERVICE_BONUS],
    [PERSONAL_BONUS]
], resize_keyboard=True)


USER_SEND_NUMBER = ReplyKeyboardMarkup([
    [SEND_NUMBER]
], resize_keyboard=True)
