class KNN():

    def __init__(self, model = None, user_id = None):
        if model is None:
            self.model = ImplicitItemKNNWrapperModel(CosineRecommender(K=10))
        else:
            self.model = model
    
        self.user_id = user_id
    
    def fit(self, df_train):

        self.model.fit(df_train)

    def recommend(self, df_train, k):

        prediction = self.model.recommend(users = self.user_id, 
                                      dataset=df_train,
                                      k = k,
                                      filter_viewed = True
                                    )
        return prediction