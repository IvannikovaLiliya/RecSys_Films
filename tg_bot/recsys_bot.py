# pip install aiogra
# python.exe -m pip install --upgrade pip
# pip install python-dotenv
# venv\Scripts\activate

import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

form_router = Router()


class Form(StatesGroup):
    exist_user_status = State()
    check_id_status = State()
    auth_ok_status = State()
    choice_genre = State()

'''
@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )
'''
data = {
    'exist_user': '',
    'current_id': 0,
    'current_genre':''
}



avaliable_user_id = [1]
rec_films = ['Фильм1','Фильм2','Фильм3']
rec_films_genre = ["Комедия","Драма","Фантастика"]

'''
Краткое описание:
1. Вопрос авторизации (если пользователь уже пользовался - НЕТ, если впервые пришел - ДА)
2. [Если 1п - НЕТ] - Задаем вопрос на проерку его id у себя в данных
3. [Если 1п - НЕТ + 2п - ввел число] - проверяем в данных, если есть пропускаем к 4п, если нет, просим ввести повторно
4. Открытие основного функционала: 
            - покажи рекомендации           - вывод рекомендаций из всех фильмов
            - покажи рекомендации по жанру  - вывод рекомендаций по жанру
            - понравится ли мне фильм?      - пользователь вводит название фильма, мы предсказываем понравится ему или нет
'''

################################################################################################################
##############################################   0. Общие ручки   ##############################################
################################################################################################################

@form_router.message(StateFilter(default_state),~Command("start"),~Command("authors"))
async def unknown_func(message: Message):
    await message.answer(text='Для работы сервиса необходимо авторизоваться (/start)\n',
                         reply_markup=ReplyKeyboardRemove())

@form_router.message(Command("authors"))
async def unknown_func(message: Message):
    await message.answer(text='Авторы бота:\nВлад Панфиленко\nЛилия Хорошенина',
                         reply_markup=ReplyKeyboardRemove())



##################################################################################################################
##############################################   1. Первый вопрос   ##############################################
##################################################################################################################

@form_router.message(Command("start"))
async def first_auth(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.exist_user_status)
    await message.answer(
        f"Привет)\n"
        f"Этот бот может рекомендовать фильмы\n"
        f"Подскажи, впервые пользуешься ботом?\n",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Да"),
                    KeyboardButton(text="Нет"),
                ]
            ],
            resize_keyboard=True,
        ),
    )

# 1.1 Первый ответ - непонятно
@form_router.message(Form.exist_user_status, ~F.text.casefold().in_(['да','нет']))
async def first_auth_err(message: Message) -> None:
    await message.answer("Я тебя не понимаю, выбери да/нет",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="Да"),
                                     KeyboardButton(text="Нет"),
                                 ]
                             ],
                             resize_keyboard=True,
                            )
                         )

# 1 -> 2 Первый ответ - НЕТ (существующий пользователь)
@form_router.message(Form.exist_user_status, F.text.casefold() == "нет")
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
    if int(message.text) in avaliable_user_id:
        await message.answer(f"Отлично, пользователь {int(message.text)}! <b>Нажмите кнопку внизу -> Меню</b>",
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
async def first_auth_unknown(message: Message, state: FSMContext) -> None:
    await message.answer(f"Некорретный ввод, введи цифры",
        reply_markup=ReplyKeyboardRemove(),
    )

# 1 -> 4 Первый ответ - ДА (новый пользователь)
@form_router.message(Form.exist_user_status, F.text.casefold() == "да")
async def first_auth_yes(message: Message, state: FSMContext) -> None:
    await state.update_data(exist_user='new')
    await state.update_data(current_id=123456)
    data = await state.get_data()
    await message.answer(
        f"Ничего страшного!\nТвой новый id {data['current_id']}\n<b>Нажмите кнопку внизу -> Меню</b>",
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
    await message.answer(text='Для начала необходимо авторизоваться (/start)',reply_markup=ReplyKeyboardRemove())



##################################################################################################################
#########################################   Переход к основному функционалу   ####################################
##################################################################################################################

# 4. Основное меню, открывается только после авторизации
@form_router.message(Form.auth_ok_status, F.text.casefold() == "меню")
async def show_summary(message: Message,state: FSMContext) -> None:
    keyboard_values = ["Покажи рекомендации","Покажи рекомендации по жанру","Понравится ли мне фильм?"]
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

@form_router.message(Form.auth_ok_status, F.text.casefold() == "покажи рекомендации")
async def list_rec_film(message: Message,state: FSMContext):
    data = await state.get_data()
    if data['exist_user'] == "new":
        current_rec_films = "\n".join(["Фильм1_для нового пользователя","Фильм2_для нового пользователя"])
    else:
        current_rec_films = "\n".join(["Фильм1_для СТАРОГО пользователя", "Фильм2_для СТАРОГО пользователя"])
    await message.answer(f'Список фильмов которые тебе понравятся:\n{current_rec_films}')


@form_router.message(Form.auth_ok_status, F.text.casefold() == "покажи рекомендации по жанру")
async def choice_genre(message: Message,state: FSMContext):
    keyboard_values = rec_films_genre
    await message.answer("Выберите жанр:",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[[KeyboardButton(text=i)] for i in keyboard_values],
                             resize_keyboard=True
                         )
                         )
    await state.set_state(Form.choice_genre)


@form_router.message(Form.choice_genre, F.text.casefold().in_(list(map(str.casefold, rec_films_genre))))
async def list_rec_film_genre(message: Message,state: FSMContext):
    await state.update_data(current_genre=message.text)
    data = await state.get_data()
    if data['exist_user'] == "new":
        current_rec_films = "\n".join(["ЖАНР_Фильм1_для нового пользователя","ЖАНР_Фильм2_для нового пользователя"])
    else:
        current_rec_films = "\n".join(["ЖАНР_Фильм1_для СТАРОГО пользователя", "ЖАНР_Фильм2_для СТАРОГО пользователя"])

    await message.answer(f"Вы ваши рекомендации по жанру {data['current_genre']}:\n"
                         f"Для возврата к меню <b>Нажмите кнопку внизу -> меню</b>",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[[KeyboardButton(text="Меню")]],
                             resize_keyboard=True
                         )
                         )
    await state.set_state(Form.auth_ok_status)


@form_router.message(Form.auth_ok_status, F.text.casefold() == "понравится ли мне фильм?")
async def predict_film(message: Message,state: FSMContext):
    await message.answer('Этот фильм в твоем вкусе')




async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())