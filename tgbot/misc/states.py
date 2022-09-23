from aiogram.dispatcher.filters.state import StatesGroup, State


class UserSignUp(StatesGroup):
    phone_number = State()


class AddAdminState(StatesGroup):
    tg_id = State()


class DeleteAdminState(StatesGroup):
    callback_state = State()


class PostPublishState(StatesGroup):
    post_name = State()
    post_title = State()
    post_preview = State()
