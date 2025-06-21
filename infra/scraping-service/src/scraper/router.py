from fastapi import APIRouter, Query

from scraper.scraper import TrackerGGScraper
from models.scraping_models import TrackerGGModel
from typing import Annotated

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
        game_mode=model.game_mode.value,
        write_to_file=False
    )

@router.post('')
async def scrape_data_with_write(model: Annotated[TrackerGGModel, Query()]):
    scraper = TrackerGGScraper()

    return await scraper.get_data_from_page(
        start_page=model.start_page,
        end_page=model.end_page, 
        platform=model.platform.value, 
        game_mode=model.game_mode.value,
        write_to_file=True
    )
