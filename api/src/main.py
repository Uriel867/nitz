from fastapi import FastAPI
from scraper.router import router as scraper_router
from reporter.router import router as reporter_router

app = FastAPI()

app.include_router(reporter_router)
app.include_router(scraper_router)

@app.get('/health')
def health():
    return 200