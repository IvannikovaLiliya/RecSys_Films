from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove


common_router = Router()


@common_router.message(StateFilter(default_state), ~Command("start"), ~Command("predict_film_test"), ~Command("authors"), ~Command("test_25"))
async def unknown_func(message: Message):
    await message.answer(text='Для работы сервиса необходимо авторизоваться (/start)\n',
                         reply_markup=ReplyKeyboardRemove())


@common_router.message(Command("authors"))
async def author_func(message: Message):
    await message.answer(text='Авторы бота:\nВлад Панфиленко\nЛилия Хорошенина',
                         reply_markup=ReplyKeyboardRemove())
