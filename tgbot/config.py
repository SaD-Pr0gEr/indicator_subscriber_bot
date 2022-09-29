import os.path
from dataclasses import dataclass
from pathlib import Path

from environs import Env


BASE_DIR = Path(__file__).resolve().parent.parent
MAIN_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"
HUMAN_READABLE_DATE_FORMAT = "дд.мм.ГГГГ!часы:минуты:секунды"
MEDIA_DIR = BASE_DIR / "media"
DRAW_PHOTOS_DIR = MEDIA_DIR / "photos/draw"
NEWS_PHOTOS_DIR = MEDIA_DIR / "photos/news"
DRAW_MEMBERS_FILE_PATH = BASE_DIR / "program_data/excel/draw_members"
USERS_QR_CODE_SAVE_PATH = MEDIA_DIR / "photos/users/qr_code"


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)
    if not os.path.exists(MEDIA_DIR):
        os.mkdir(MEDIA_DIR)
    if not os.path.exists(DRAW_PHOTOS_DIR):
        os.makedirs(DRAW_PHOTOS_DIR)
    if not os.path.exists(NEWS_PHOTOS_DIR):
        os.makedirs(NEWS_PHOTOS_DIR)
    if not os.path.exists(DRAW_MEMBERS_FILE_PATH):
        os.makedirs(DRAW_MEMBERS_FILE_PATH)
    if not os.path.exists(USERS_QR_CODE_SAVE_PATH):
        os.makedirs(USERS_QR_CODE_SAVE_PATH)
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.str("ADMINS").split(","))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous()
    )
