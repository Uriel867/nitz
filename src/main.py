from fastapi import FastAPI
from mongo.router import router as mongo_router

app = FastAPI()

app.include_router(mongo_router)
