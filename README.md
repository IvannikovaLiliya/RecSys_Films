# RecSys_Films
Репозиторий проекта рекомендательных систем по фильмам:    
- Краткое ревью в презентации [RecSys - презентация.pdf](https://github.com/IvannikovaLiliya/RecSys_Films/blob/master/RecSys%20-%20%D0%BF%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F.pdf);
- [app](app) - приложение fastapi + тг-бот;
- [EDA](EDA) - первичный анализ данных;
- [recsyc_part1](recsyc_part1) - финальные модели;
- [tests](tests) - тесты и все что с ними связано.

# Запуск бота
- необходимо клонировать репозиторий на локальную машину;
- находясь в корневой директории прописать в консоли ```docker compose up --build```
    
### План проекта (может корректироваться):    
[Ссылка на google-документ](https://docs.google.com/document/d/1ErzQ7lf4dIpijgG4vmwcGSvy3dYz9V8db09wqW16Frw/edit?usp=sharing)
    
    
### Структура данных:    
[Ссылка на google-таблицу](https://docs.google.com/spreadsheets/d/1feZpmxxlIWfJ4-VrLrBzTngBFMFNwXb2b1ocfvsFezI/edit?usp=sharing)
    
    
### Датасеты:
Используется датасет movielens https://files.grouplens.org/datasets/movielens/ml-latest-README.html    
[Ссылка на google-диск с датасетом](https://drive.google.com/file/d/1cOOnSeXrYxYDrmAySUNxFiFlOMzczJD2/view?usp=sharing)
    
Дополнительно используется датасет imdb https://developer.imdb.com/non-commercial-datasets/    
[Ссылка на google-диск с датасетом](https://drive.google.com/file/d/1JSpzTZKUJVA3HwO7b1E80ld6dPwUoNB3/view?usp=sharing)
    
Данные для модели, построенной на базе библиотеки LightFm    
[Ссылка на google-диск с файлами по модели](https://drive.google.com/drive/folders/1hIhQTeSNQ3oCJTboDrya0sFCFuPmKKmq?usp=sharing)
