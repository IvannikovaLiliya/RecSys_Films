import pytest
from aiogram.filters import Command
from aiogram.methods import SendMessage
from app.bot_handlers.schemas import Form
from app.bot_handlers.common import author_func, unknown_func
from app.bot_handlers.handler_auth import (first_auth, first_auth_err, first_auth_no,
                                           first_auth_no_check_id, first_auth_unknown,
                                           first_auth_yes, send_chouse_film)
from app.bot_handlers.handler_main_menu import (show_summary, list_rec_film,
                                                choice_genre, list_rec_film_genre,
                                                predict_film)
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_unknown_func():
    requester = MockedBot(request_handler=MessageHandler(unknown_func))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text=""))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'Для работы сервиса необходимо авторизоваться (/start)\n'


@pytest.mark.asyncio
async def test_author_func():
    requester = MockedBot(request_handler=MessageHandler(author_func, Command(commands=["authors"])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="/authors"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'Авторы бота:\nВлад Панфиленко\nЛилия Хорошенина'


@pytest.mark.asyncio
async def test_first_auth():
    requester = MockedBot(request_handler=MessageHandler(first_auth, Command(commands=["start"])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == (f"Привет)\n"
        f"Этот бот может рекомендовать фильмы\n"
        f"Подскажи, впервые пользуешься ботом?\n")


@pytest.mark.asyncio
async def test_first_auth_err():
    requester = MockedBot(request_handler=MessageHandler(first_auth_err, state=Form.exist_user_status))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text=""))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == ('Я тебя не понимаю, выбери одну из предложенных кнопок ниже')


@pytest.mark.asyncio
async def test_first_auth_no():
    requester = MockedBot(request_handler=MessageHandler(first_auth_no, state=Form.exist_user_status))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="нет, уже пользовался"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == ('Введи свой id чтобы мы могли узнать тебя:')


@pytest.mark.asyncio
async def test_first_auth_no_check_id():
    requester = MockedBot(request_handler=MessageHandler(first_auth_no_check_id, state=Form.check_id_status))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="1010"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == (f"Отлично, пользователь 1010!\n\n<b>Нажмите кнопку внизу -> Меню</b>")
    calls = await requester.query(MESSAGE.as_object(text="1"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == ("Нет такого пользователя")


@pytest.mark.asyncio
async def test_first_auth_unknown():
    requester = MockedBot(request_handler=MessageHandler(first_auth_unknown, state=Form.check_id_status))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="abc"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == ("Некорректный ввод, введи цифры")


@pytest.mark.asyncio
async def test_first_auth_yes():
    requester = MockedBot(request_handler=MessageHandler(first_auth_yes, state=Form.exist_user_status))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="123456"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == (f"Ничего страшного!\nТвой новый id 123456\n\n<b>Нажмите кнопку внизу -> Меню</b>")


@pytest.mark.asyncio
async def test_send_chouse_film():
    requester = MockedBot(request_handler=MessageHandler(send_chouse_film, state=Form.exist_user_status))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text=""))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == ("Для начала необходимо авторизоваться (/start)")


@pytest.mark.asyncio
async def test_show_summary():
    requester = MockedBot(MessageHandler(show_summary,
                                         state=Form.auth_ok_status,
                                         state_data={"exist_user": "new"}
                                         )
                          )
    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Чем могу помочь?"
    requester = MockedBot(MessageHandler(show_summary,
                                         state=Form.auth_ok_status,
                                         state_data={"exist_user": "old"}
                                         )
                          )
    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Чем могу помочь?"


@pytest.mark.asyncio
async def test_list_rec_film():
    requester = MockedBot(MessageHandler(list_rec_film,
                                         state=Form.auth_ok_status,
                                         state_data={"exist_user": "new"}
                                         )
                          )
    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone().text
    assert answer_message == (f"Список фильмов которые тебе понравятся:\n\nПобег из Шоушенка\nBBC: Планета Земля\nКрёстный отец\nПаразиты\nБратья по оружию")
    requester = MockedBot(MessageHandler(list_rec_film,
                                         state=Form.auth_ok_status,
                                         state_data={"exist_user": "old",
                                                     "current_id": 1010}
                                         )
                          )
    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone().text
    assert answer_message == (
        f"Список фильмов которые тебе понравятся:\n\nМузей Маргариты\nШоссе\nЛуна-соблазнительница\nЗамена\nApollon 13")


@pytest.mark.asyncio
async def test_choice_genre():
    requester = MockedBot(request_handler=MessageHandler(choice_genre, state=Form.auth_ok_status))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text=""))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == ("Выберите жанр:")


@pytest.mark.asyncio
async def test_list_rec_film_genre():
    requester = MockedBot(MessageHandler(list_rec_film_genre,
                                         state=Form.choice_genre,
                                         state_data={"exist_user": "new"}
                                         )
                          )
    calls = await requester.query(MESSAGE.as_object(text="Романтика"))
    answer_message = calls.send_message.fetchone().text

    assert answer_message == (
        f"Вы ваши рекомендации по жанру Романтика:\n\nCasablanca\nЖизнь других\nНа север через северо-запад\nСансет бульвар\nЖизнь прекрасна\n\nДля возврата к меню <b>Нажмите кнопку внизу -> меню</b>"
    )

    requester = MockedBot(MessageHandler(list_rec_film_genre,
                                         state=Form.choice_genre,
                                         state_data={"exist_user": "old",
                                                     "current_id": 1010}
                                         )
                          )
    calls = await requester.query(MESSAGE.as_object(text="Нуар"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == (
        f"Вы ваши рекомендации по жанру Нуар:\n\nДьявол в голубом платье\nСансет бульвар\nЛора\nForeign Correspondent\nGilda\n\nДля возврата к меню <b>Нажмите кнопку внизу -> меню</b>"
    )


@pytest.mark.asyncio
async def test_predict_film():
    requester = MockedBot(request_handler=MessageHandler(predict_film, state=Form.auth_ok_status))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="понравится ли мне фильм?"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'TBD: будет показывать понравится ли тебе фильм или нет'
