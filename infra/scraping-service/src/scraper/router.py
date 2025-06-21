from fastapi import APIRouter, Query
from typing import Annotated

from scraper.scraper import TrackerGGScraper
from models.models import TrackerGGModel


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

@router.post('')
async def scrape_data_with_write(model: Annotated[TrackerGGModel, Query()]):
    scraper = TrackerGGScraper()

    return await scraper.get_data_from_page(
        start_page=model.start_page,
        end_page=model.end_page, 
        platform=model.platform.value, 
        game_mode=model.game_mode.value
    )
