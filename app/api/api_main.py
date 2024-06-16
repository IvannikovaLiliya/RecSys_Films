from fastapi import FastAPI, HTTPException
from ml_model.LightFMClass import model_recomend, genre_list

app1 = FastAPI()


@app1.post("/rec_auth")
async def give_rec(user: int):
    return model_recomend(user, None)


@app1.post("/rec_genre_auth")
async def give_rec_genre(user: int, genre: str):
    if genre.title() not in genre_list:
        raise HTTPException(status_code=404, detail=f"Неправильный жанр, вы можете выбрать: {genre_list}")
    return model_recomend(user, genre)


@app1.get("/rec_nonauth")
async def give_rec():
    return model_recomend(123456789, None)


@app1.post("/rec_genre_nonauth")
async def give_rec_genre(genre: str):
    if genre.title() not in genre_list:
        raise HTTPException(status_code=404, detail=f"Неправильный жанр, вы можете выбрать: {genre_list}")
    return model_recomend(123456789, genre)
