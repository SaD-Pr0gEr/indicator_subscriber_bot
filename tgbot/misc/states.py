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


class AddDrawState(StatesGroup):
    name = State()
    title = State()
    photo = State()
    start_date = State()
    end_date = State()
    winners_count = State()


class CancelDrawState(StatesGroup):
    draw = State()
    confirm = State()


class ParticipateDrawState(StatesGroup):
    choose_draw = State()


class GetDrawInfoState(StatesGroup):
    choose_draw = State()


class UserBonusesState(StatesGroup):
    choose_command = State()
    choose_bonus_type = State()
    personal_bonus = State()
