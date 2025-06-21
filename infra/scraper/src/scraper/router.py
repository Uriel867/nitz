from fastapi import APIRouter, Query, Depends
from typing import Annotated

from .scraper import TrackerGGScraper
from .models import TrackerGGModel

from di.dependencies import get_scraper


router = APIRouter(
    prefix='/scrape'
)

# defining an annotated type to reuse in multiple endpoints
Scraper = Annotated[TrackerGGScraper, Depends(get_scraper)]

@router.get('')
async def scrape_data(model: Annotated[TrackerGGModel, Query()], scraper: Scraper):
    return await scraper.get_data_from_page(
        start_page=model.start_page,
        end_page=model.end_page, 
        platform=model.platform, 
        game_mode=model.game_mode
    )
