from fastapi import FastAPI
from reporter.router import router as reporter_router

app = FastAPI()

app.include_router(reporter_router)
