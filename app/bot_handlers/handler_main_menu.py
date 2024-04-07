import requests
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from bot_handlers.schemas import Form, rec_films_genre, genre_dict

menu_router = Router()

#url_domain = '127.0.0.1:8000'
url_domain = 'api:8000'

# 4. Основное меню, открывается только после авторизации
@menu_router.message(Form.auth_ok_status, F.text.casefold() == "меню")
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
@menu_router.message(Form.auth_ok_status, F.text.casefold() == "покажи рекомендации")
async def list_rec_film(message: Message, state: FSMContext):
    data = await state.get_data()
    if data['exist_user'] == "new":
        response = requests.get(f"http://{url_domain}/rec_nonauth")
        current_rec_films = "\n".join(response.json())
    else:
        response = requests.post(f"http://{url_domain}/rec_auth?user={data['current_id']}")
        current_rec_films = "\n".join(response.json())
    await message.answer(f'Список фильмов которые тебе понравятся:\n\n{current_rec_films}')


# 4.2 Ручка "жанровых" рекомендаций, делится на "холодных" и "обычных пользователе"
@menu_router.message(Form.auth_ok_status, F.text.casefold() == "покажи рекомендации по жанру")
async def choice_genre(message: Message, state: FSMContext):
    keyboard_values = rec_films_genre
    await message.answer("Выберите жанр:",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[[KeyboardButton(text=i)] for i in keyboard_values],
                             resize_keyboard=True
                         )
                         )
    await state.set_state(Form.choice_genre)


@menu_router.message(Form.choice_genre, F.text.casefold().in_(list(map(str.casefold, rec_films_genre))))
async def list_rec_film_genre(message: Message, state: FSMContext):
    await state.update_data(current_genre=message.text)
    data = await state.get_data()
    genre=genre_dict.get(data['current_genre'])
    if data['exist_user'] == "new":
        response = requests.post(f"http://{url_domain}/rec_genre_nonauth?genre={genre}")
        current_rec_films = "\n".join(response.json())
    else:
        response = requests.post(f"http://{url_domain}/rec_genre_auth?user={data['current_id']}&genre={genre}")
        current_rec_films = "\n".join(response.json())

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
@menu_router.message(Form.auth_ok_status, F.text.casefold() == "понравится ли мне фильм?")
async def predict_film(message: Message):
    await message.answer('TBD: будет показывать понравится ли тебе фильм или нет')
