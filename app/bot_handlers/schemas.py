from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    exist_user_status = State()
    check_id_status = State()
    auth_ok_status = State()
    choice_genre = State()


rec_films_genre = ['Анимация', 'Вестерн', 'Военный', 'Детский', 'Документальный',
                   'Драма', 'Комедия', 'Криминал', 'Мистика', 'Мюзикл', 'Нуар',
                   'Приключения', 'Романтика', 'Триллер', 'Ужасы', 'Фантастика', 'Фэнтези', 'Экшен'
                   ]

genre_dict = {
    "Экшен": "action",
    "Приключения": "adventure",
    "Анимация": "animation",
    "Детский": "children's",
    "Комедия": "comedy",
    "Криминал": "crime",
    "Документальный": "documentary",
    "Драма": "drama",
    "Фэнтези": "dantasy",
    "Нуар": "film-Noir",
    "Ужасы": "horror",
    "Мюзикл": "musical",
    "Мистика": "mystery",
    "Романтика": "romance",
    "Фантастика": "sci-Fi",
    "Триллер": "thriller",
    "Военный": "war",
    "Вестерн": "western"
}