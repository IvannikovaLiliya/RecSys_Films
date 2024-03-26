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

from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from dotenv import load_dotenv

from LightFMClass import LightFMRecSyc, moveis_fin, movies_to_predict, RecSycFilms, ClassRecSyc

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

form_router = Router()


class Form(StatesGroup):
    exist_user_status = State()
    check_id_status = State()
    auth_ok_status = State()
    choice_genre = State()


'''
data = {
    'exist_user': '',
    'current_id': 0,
    'current_genre': ''
}
'''

avaliable_user_id = [195, 1010, 7438, 30323, 30349]
rec_films = ['Фильм1', 'Фильм2', 'Фильм3']
rec_films_genre = ['Анимация', 'Вестерн', 'Военный', 'Детский', 'Документальный',
                   'Драма', 'Комедия', 'Криминал', 'Мистика', 'Мюзикл', 'Нуар',
                   'Приключения', 'Романтика', 'Триллер', 'Ужасы', 'Фантастика', 'Фэнтези', 'Экшен'
                   ]

genre_dict = {
    "Экшен": "Action",
    "Приключения": "Adventure",
    "Анимация": "Animation",
    "Детский": "Children's",
    "Комедия": "Comedy",
    "Криминал": "Crime",
    "Документальный": "Documentary",
    "Драма": "Drama",
    "Фэнтези": "Fantasy",
    "Нуар": "Film-Noir",
    "Ужасы": "Horror",
    "Мюзикл": "Musical",
    "Мистика": "Mystery",
    "Романтика": "Romance",
    "Фантастика": "Sci-Fi",
    "Триллер": "Thriller",
    "Военный": "War",
    "Вестерн": "Western"
}
'''
Краткое описание:
1. Вопрос авторизации (если пользователь уже пользовался - НЕТ, если впервые пришел - ДА)
2. [Если 1п - НЕТ] - Задаем вопрос на проверку его id у себя в данных
3. [Если 1п - НЕТ + 2п - ввел число] - проверяем в данных, если есть пропускаем к 4п, если нет, просим ввести повторно
4. Открытие основного функционала:
            - покажи рекомендации           - вывод рекомендаций из всех фильмов
            - покажи рекомендации по жанру  - вывод рекомендаций по жанру
            - понравится ли мне фильм?      - TBD пользователь вводит название фильма, мы предсказываем понравится/нет
'''

'''
 ----------------------------------------------------------------------------------------------------------------
---------------------------------------------   0. Общие ручки   ------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
'''


@form_router.message(StateFilter(default_state), ~Command("start"), ~Command("authors"), ~Command("test_25"))
async def unknown_func(message: Message):
    await message.answer(text='Для работы сервиса необходимо авторизоваться (/start)\n',
                         reply_markup=ReplyKeyboardRemove())


@form_router.message(Command("authors"))
async def author_func(message: Message):
    await message.answer(text='Авторы бота:\nВлад Панфиленко\nЛилия Хорошенина',
                         reply_markup=ReplyKeyboardRemove())


'''
 ----------------------------------------------------------------------------------------------------------------
---------------------------------------------   1. Первый вопрос   ----------------------------------------------
-----------------------------------------------------------------------------------------------------------------
'''


@form_router.message(Command("start"))
async def first_auth(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.exist_user_status)
    await message.answer(
        "Привет)\n"
        "Этот бот может рекомендовать фильмы\n"
        "Подскажи, впервые пользуешься ботом?\n",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Да, я новый пользователь"),
                    KeyboardButton(text="Нет, уже пользовался"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


# 1.1 Первый ответ - непонятно
@form_router.message(Form.exist_user_status,
                     ~F.text.casefold().in_(['да, я новый пользователь', 'нет, уже пользовался']))
async def first_auth_err(message: Message) -> None:
    await message.answer("Я тебя не понимаю, выбери одну из предложенных кнопок ниже",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="Да, я новый пользователь"),
                                     KeyboardButton(text="Нет, уже пользовался"),
                                 ]
                             ],
                             resize_keyboard=True,
                         )
                         )


# 1 -> 2 Первый ответ - НЕТ (существующий пользователь)
@form_router.message(Form.exist_user_status, F.text.casefold() == "нет, уже пользовался")
async def first_auth_no(message: Message, state: FSMContext) -> None:
    await state.update_data(exist_user='old')
    await message.answer(
        "Введи свой id чтобы мы могли узнать тебя:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Form.check_id_status)


# 2 -> 4 первый ответ проверка id и переход к меню ИЛИ 2 -> 3 первый ответ проверка id - не найден id
@form_router.message(Form.check_id_status, F.text.isdigit())
async def first_auth_no_check_id(message: Message, state: FSMContext) -> None:
    await state.update_data(current_id=int(message.text))
    data = await state.get_data()
    if int(message.text) in avaliable_user_id:
        await message.answer(f"Отлично, пользователь {data['current_id']}!\n\n<b>Нажмите кнопку внизу -> Меню</b>",
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=[[KeyboardButton(text="Меню")]],
                                 resize_keyboard=True,
                             )
                             )
        await state.set_state(Form.auth_ok_status)
    else:
        await message.answer('Нет такого пользователя')


# 3 первый ответ проверка id - не найден id
@form_router.message(Form.check_id_status, ~F.text.isdigit())
async def first_auth_unknown(message: Message) -> None:
    await message.answer("Некорректный ввод, введи цифры",
                         reply_markup=ReplyKeyboardRemove(),
                         )


# 1 -> 4 Первый ответ - ДА (новый пользователь)
@form_router.message(Form.exist_user_status, F.text.casefold() == "да, я новый пользователь")
async def first_auth_yes(message: Message, state: FSMContext) -> None:
    await state.update_data(exist_user='new')
    await state.update_data(current_id=123456)
    data = await state.get_data()
    await message.answer(
        f"Ничего страшного!\nТвой новый id {data['current_id']}\n\n<b>Нажмите кнопку внизу -> Меню</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Меню")
                ]
            ],
            resize_keyboard=True,
        )
    )
    await state.set_state(Form.auth_ok_status)


# ??? ПРОМЕЖУТОЧНАЯ РУЧКА - если пользователь не авторизовался и хочет дергать основные функции
@form_router.message(~StateFilter(Form.auth_ok_status),
                     F.text.casefold().in_(["покажи рекомендации",
                                            "покажи рекомендации по жанру",
                                            "понравится ли мне фильм?"])
                     )
async def send_chouse_film(message: Message):
    await message.answer(text='Для начала необходимо авторизоваться (/start)', reply_markup=ReplyKeyboardRemove())


'''
 ----------------------------------------------------------------------------------------------------------------
-------------------------------------   2. Переход к основному функционалу   ------------------------------------
-----------------------------------------------------------------------------------------------------------------
'''


# 4. Основное меню, открывается только после авторизации
@form_router.message(Form.auth_ok_status, F.text.casefold() == "меню")
async def show_summary(message: Message, state: FSMContext) -> None:
    keyboard_values = ["Покажи рекомендации", "Покажи рекомендации по жанру", "Понравится ли мне фильм?"]
    data = await state.get_data()
    if data['exist_user'] == "new":
        await message.answer("Чем могу помочь?",
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=[[KeyboardButton(text=i)] for i in keyboard_values[:-1]],
                                 resize_keyboard=True
                             )
                             )
    else:
        await message.answer("Чем могу помочь?",
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=[[KeyboardButton(text=i)] for i in keyboard_values],
                                 resize_keyboard=True
                             )
                             )


# 4.1 Ручка обычных рекомендаций, делиться на "холодных" и "обычных пользователе"
@form_router.message(Form.auth_ok_status, F.text.casefold() == "покажи рекомендации")
async def list_rec_film(message: Message, state: FSMContext):
    data = await state.get_data()
    lfm = LightFMRecSyc(model=ClassRecSyc,
                        RecSycFilms=RecSycFilms,
                        IMDb_df=moveis_fin,
                        Genre=None)
    if data['exist_user'] == "new":
        result = lfm.recommend(user_id=[123456789], k=5, movies_to_predict=movies_to_predict)
        current_rec_films = "\n".join(result)
    else:
        result = lfm.recommend(user_id=[data['current_id']], k=5, movies_to_predict=movies_to_predict)
        current_rec_films = "\n".join(result)
    await message.answer(f'Список фильмов которые тебе понравятся:\n\n{current_rec_films}')


# 4.2 Ручка "жанровых" рекомендаций, делиться на "холодных" и "обычных пользователе"
@form_router.message(Form.auth_ok_status, F.text.casefold() == "покажи рекомендации по жанру")
async def choice_genre(message: Message, state: FSMContext):
    keyboard_values = rec_films_genre
    await message.answer("Выберите жанр:",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[[KeyboardButton(text=i)] for i in keyboard_values],
                             resize_keyboard=True
                         )
                         )
    await state.set_state(Form.choice_genre)


@form_router.message(Form.choice_genre, F.text.casefold().in_(list(map(str.casefold, rec_films_genre))))
async def list_rec_film_genre(message: Message, state: FSMContext):
    await state.update_data(current_genre=message.text)
    data = await state.get_data()
    lfm = LightFMRecSyc(model=ClassRecSyc,
                        RecSycFilms=RecSycFilms,
                        IMDb_df=moveis_fin,
                        Genre=genre_dict.get(data['current_genre']))
    if data['exist_user'] == "new":
        result = lfm.recommend(user_id=[123456789], k=5, movies_to_predict=movies_to_predict)
        current_rec_films = "\n".join(result)
    else:
        result = lfm.recommend(user_id=[data['current_id']], k=5, movies_to_predict=movies_to_predict)
        current_rec_films = "\n".join(result)

    await message.answer(f"Вы ваши рекомендации по жанру {data['current_genre']}:\n\n"
                         f"{current_rec_films}\n\n"
                         f"Для возврата к меню <b>Нажмите кнопку внизу -> меню</b>",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[[KeyboardButton(text="Меню")]],
                             resize_keyboard=True
                         )
                         )
    await state.set_state(Form.auth_ok_status)


# 4.3 Ручка предсказания фильма (TBD), делить на "холодных" и "обычных пользователе"
@form_router.message(Form.auth_ok_status, F.text.casefold() == "понравится ли мне фильм?")
async def predict_film(message: Message):
    await message.answer('TBD: будет показывать понравится ли тебе фильм или нет')


# вариант для локального запуска

async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

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


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(url=WEBHOOK_URL)


def main() -> None:
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.include_router(form_router)
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
'''
