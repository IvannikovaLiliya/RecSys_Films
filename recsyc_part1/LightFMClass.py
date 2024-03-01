import pandas as pd
import pickle
import numpy as np


class LightFM_Rec():

    def __init__(self, model=None, Rec_films=None, IMDb_df=None, Genre=None):

        '''
        model - наша модель LightFM
        IMDb_df - данные для холодного старта
        Genre - жанр, в рамках которого необходима рек-ия
        Rec_films - фильмы для рек-ии
        '''

        self.model = model
        self.IMDb_df = IMDb_df
        self.Genre = Genre
        self.Rec_films = Rec_films

    def IMDb(self):
        """
            Обработка кейсов, когда нет оценок по user_id
        """
        if self.Genre is None:
            return self.IMDb_df['TITLE']
        else:
            return self.IMDb_df.loc[self.IMDb_df[self.Genre] == 1, 'TITLE']

    def recommend(self, user_id, k, movies_to_predict):
        """
            Расчет рекомендаций
        """
        # Если ранее такого пользователя не было, используем IMDb
        try:

            prediction = self.model.predict(user_ids=user_id * len(movies_to_predict),
                                            item_ids=movies_to_predict
                                            )
            dict_items = dict(zip(movies_to_predict, prediction))

            if self.Genre is None:

                items_s = list(dict(sorted(dict_items.items(), key=lambda item: item[1], reverse=True)).keys())[:k]

            else:

                genre_films = moveis_fin.loc[moveis_fin[self.Genre] == 1, 'MOVIEID'].to_list()
                set_films = set(dict_items.keys()) & set(genre_films)
                dict_genre = {key: dict_items[key] for key in list(set_films)}
                items_s = list(dict(sorted(dict_genre.items(), key=lambda item: item[1], reverse=True)).keys())[:k]

            predict = list()

            for movie in range(0, k):
                predict.append(self.Rec_films.loc[self.Rec_films['item_id'].isin([items_s[movie]]),
                'TITLE'].item())
            return predict

        except:
            return self.IMDb()[:k].to_list()


Rec_films = pd.read_csv('RecSycFilms.csv', sep='\t', index_col=0)
moveis_fin = pd.read_csv('IMDb.csv', sep='\t', index_col=0)

with open("movies_to_predict", "rb") as fp:  # Unpickling
    movies_to_predict = pickle.load(fp)

ClassRecSyc = pickle.load(open('lfm_model_fin_v2.pkl.pkl', 'rb'))

# без жанра
lfm = LightFM_Rec(model=ClassRecSyc, RecSycFilms=Rec_films,
                    IMDb_df=moveis_fin, Genre=None)
lfm.recommend(user_id = [274724], k = 5, movies_to_predict = movies_to_predict)

# с жанром
lfm = LightFM_Rec(model=ClassRecSyc, RecSycFilms=Rec_films,
                    IMDb_df=moveis_fin, Genre='Drama')
lfm.recommend(user_id = [274724], k = 5, movies_to_predict = movies_to_predict)
