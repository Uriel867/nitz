from fastapi import APIRouter, Query
from typing import Annotated

from .scraper import TrackerGGScraper
from .models import TrackerGGModel


router = APIRouter(
    prefix='/scrape'
)

@router.get('')
async def scrape_data(model: Annotated[TrackerGGModel, Query()]):
    scraper = TrackerGGScraper()

    return await scraper.get_data_from_page(
        start_page=model.start_page,
        end_page=model.end_page, 
        platform=model.platform.value, 
        game_mode=model.game_mode.value
    )
