import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config, BASE_DIR, Config
from tgbot.filters import register_all_filters
from tgbot.handlers import register_all_handlers
from tgbot.models.models import db
from tgbot.utils.mailing import draw_monitoring

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    config: Config = bot['config']
    for i in config.tg_bot.admin_ids:
        await bot.send_message(
            i,
            "Бот запущен! Идёт проверка и обновление розыгрышей"
        )


async def on_shutdown(dp: Dispatcher):
    config: Config = dp.bot['config']
    for i in config.tg_bot.admin_ids:
        await dp.bot.send_message(
            i,
            "Бот остановился! Проверьте сервер если сами её не отключили!\n"
            "После запуска бот проверит и обновит все розыгрышы"
        )


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u"%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config(str(BASE_DIR / ".env"))

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)

    bot["config"] = config

    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await db.set_bind(f"postgresql://"
                          f"{config.db.user}:{config.db.password}@"
                          f"{config.db.host}:5432/{config.db.database}")
        await on_startup(bot)
        loop = asyncio.get_event_loop()
        task_1 = loop.create_task(draw_monitoring(bot, loop))
        task_2 = loop.create_task(dp.start_polling())
        await asyncio.gather(task_1, task_2)
        await on_shutdown(dp)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        await db.pop_bind().close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
