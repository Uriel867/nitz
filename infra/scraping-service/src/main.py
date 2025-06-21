from fastapi import FastAPI

from scraper.router import router as scraper_router

app = FastAPI()

app.include_router(scraper_router)
