from fastapi import FastAPI
from api.matches.router import router as match_router
from api.summoners.router import router as summoners_router

app = FastAPI()

app.include_router(match_router)
app.include_router(summoners_router)