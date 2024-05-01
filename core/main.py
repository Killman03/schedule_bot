from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import asyncio
import logging

from aiogram.filters import Command

from core.settings import settings
from core.handlers.commands import set_commands
from core.handlers.basic import get_next_lesson
from core.middlewares.apschedulemiddleware import SchedulerMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import sys
from core.utils.webscraper import send_lessons
import time
from core.utils.webscraper import BotWindow
from aiogram.types import message



async def on_startup(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.ADMIN_ID, text='Bot is running')


async def on_shutdown(bot: Bot):
    await bot.send_message(settings.bots.ADMIN_ID, text='Bot shut down')


async def start():
    bot = Bot(
        token=settings.bots.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    # schedule.every().day.at("11:50").do(send_message)
    # schedule.every().day.at("13:20").do(send_message)


    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Asia/Bishkek")
    #scheduler.add_job(get_next_lesson, trigger='interval', seconds=10, kwargs={'bot': bot})
    scheduler.start()
    dp.startup.register(on_startup)
    #dp.update.register(SchedulerMiddleware)
    dp.message.register(get_next_lesson, Command(commands=['next_lesson']))
    dp.shutdown.register(on_shutdown)

    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
    bot = BotWindow(use_proxy=True, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
