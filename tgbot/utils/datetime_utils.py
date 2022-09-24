import asyncio
from typing import Union

from tgbot.models.models import Draw


async def sleep_and_activate_draw(draw: Draw, sleep_time: Union[int, float]):
    await asyncio.sleep(sleep_time)
    await draw.update(active=True).apply()


async def sleep_and_deactivate_draw(draw: Draw, sleep_time: Union[int, float]):
    await asyncio.sleep(sleep_time)
    await draw.update(active=False).apply()
