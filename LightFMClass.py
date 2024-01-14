import pandas as pd
import pickle


class LightFMRecSyc():

    def __init__(self, model=None, RecSycFilms=None, IMDb_df=None, Genre=None):

        self.model = model
        self.IMDb_df = IMDb_df
        self.Genre = Genre
        self.RecSycFilms = RecSycFilms

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

            n_movies = self.RecSycFilms['item_id'].unique()

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
                predict.append(self.RecSycFilms.loc[self.RecSycFilms['item_id'].isin([items_s[movie]]),
                'TITLE'].item())
            return predict

        except:
            return self.IMDb()[:k].to_list()


RecSycFilms = pd.read_csv('RecSycFilms.csv', sep='\t', index_col=0)
moveis_fin = pd.read_csv('IMDb.csv', sep='\t', index_col=0)

with open("movies_to_predict", "rb") as fp:  # Unpickling
    movies_to_predict = pickle.load(fp)

ClassRecSyc = pickle.load(open('model_pred.pkl', 'rb'))

# без жанра
lfm = LightFMRecSyc(model=ClassRecSyc, RecSycFilms=RecSycFilms,
                    IMDb_df=moveis_fin, Genre=None)
lfm.recommend(user_id = [274724], k = 5, movies_to_predict = movies_to_predict)

# с жанром
lfm = LightFMRecSyc(model=ClassRecSyc, RecSycFilms=RecSycFilms,
                    IMDb_df=moveis_fin, Genre='Drama')
lfm.recommend(user_id = [274724], k = 5, movies_to_predict = movies_to_predict)