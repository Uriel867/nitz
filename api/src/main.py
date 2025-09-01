from fastapi import  FastAPI
from reporter.router import router as reporter_router
from riot_games.router import router as riot_games_router

app = FastAPI()

app.include_router(reporter_router)
app.include_router(riot_games_router)


