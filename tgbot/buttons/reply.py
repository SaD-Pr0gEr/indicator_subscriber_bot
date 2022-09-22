from aiogram.types import KeyboardButton

from tgbot.data.commands import COMMANDS

ADD_ADMIN = KeyboardButton(COMMANDS["add_admin"])
SUBSCRIBERS_LIST = KeyboardButton(COMMANDS["subscribers_list"])
ADMINS_LIST = KeyboardButton(COMMANDS["admins_list"])
KICK_ADMIN = KeyboardButton(COMMANDS["kick_admin"])
CALL_US = KeyboardButton(COMMANDS["call_us"])
SEND_NUMBER = KeyboardButton(COMMANDS["send_number"], request_contact=True)