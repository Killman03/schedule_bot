from aiogram import Bot
from aiogram.types import Message
import csv
from core.settings import settings
from core.utils.webscraper import send_lessons


# Rewrite it in the future to webscraper.py
def send_first_cell():
    with open(r'C:\Users\user\PycharmProjects\schedule_bot\core\utils\ajk.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        first_row = next(reader)  # Получаем первую строку
        return f'{first_row[0]} {first_row[2]} будет в {first_row[1]}'


async def get_next_lesson(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'{send_lessons()}')
