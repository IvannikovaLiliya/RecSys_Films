# pip install aiogram
# python.exe -m pip install --upgrade pip
# pip install python-dotenv

# pip install aiogram==3.0.0b7
# pip install pytest==7.4.4
# pip install pytest-asyncio==0.23.4
# aiogram_tests скачать папку и закинуть в директорию
# pip install coverage
# coverage run -m pytest test_bot.py
# coverage report -m
# coverage html
# coverage erase


import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from bot_handlers.common import common_router
from bot_handlers.handler_auth import auth_router
from bot_handlers.handler_main_menu import menu_router


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


# вариант для локального запуска

async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(common_router)
    dp.include_router(auth_router)
    dp.include_router(menu_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
'''
# вариант с вебхуком для хостинга
BASE_WEBHOOK_URL = ''
WEBHOOK_HOST = 'https://pvv-bot-aiogram.onrender.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEB_SERVER_HOST = '0.0.0.0'
WEB_SERVER_PORT = 10000


async def on_startup(app: Bot) -> None:
    await app.set_webhook(url=WEBHOOK_URL)


def main() -> None:
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.include_router(form_router)
    app = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        app=app
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, app=app)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
'''
