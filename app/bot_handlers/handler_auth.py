from aiogram import F, Router
from aiogram.enums import ParseMode
from bot_handlers.schemas import Form
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.fsm.state import State, StatesGroup


auth_router = Router()
avaliable_user_id = [195, 1010, 7438, 30323, 30349]

@auth_router.message(Command("start"))
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
@auth_router.message(Form.exist_user_status,
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
@auth_router.message(Form.exist_user_status, F.text.casefold() == "нет, уже пользовался")
async def first_auth_no(message: Message, state: FSMContext) -> None:
    await state.update_data(exist_user='old')
    await message.answer(
        "Введи свой id чтобы мы могли узнать тебя:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Form.check_id_status)


# 2 -> 4 первый ответ проверка id и переход к меню ИЛИ 2 -> 3 первый ответ проверка id - не найден id
@auth_router.message(Form.check_id_status, F.text.isdigit())
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
@auth_router.message(Form.check_id_status, ~F.text.isdigit())
async def first_auth_unknown(message: Message) -> None:
    await message.answer("Некорректный ввод, введи цифры",
                         reply_markup=ReplyKeyboardRemove(),
                         )


# 1 -> 4 Первый ответ - ДА (новый пользователь)
@auth_router.message(Form.exist_user_status, F.text.casefold() == "да, я новый пользователь")
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


# ПРОМЕЖУТОЧНАЯ РУЧКА - если пользователь не авторизовался и хочет дергать основные функции
@auth_router.message(~StateFilter(Form.auth_ok_status),
                     F.text.casefold().in_(["покажи рекомендации",
                                            "покажи рекомендации по жанру",
                                            "понравится ли мне фильм?"])
                     )
async def send_chouse_film(message: Message):
    await message.answer(text='Для начала необходимо авторизоваться (/start)', reply_markup=ReplyKeyboardRemove())
