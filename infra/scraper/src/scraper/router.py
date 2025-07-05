from fastapi import APIRouter, Query, Depends
from typing import Annotated

from .service import LeagueOfGraphsScraper
from .models import LeagueOfGraphsModel

from di.dependencies import get_scraper


router = APIRouter(
    prefix='/scrape'
)

# defining an annotated type to reuse in multiple endpoints
Scraper = Annotated[LeagueOfGraphsScraper, Depends(get_scraper)]

@router.get('')
async def scrape_data(model: Annotated[LeagueOfGraphsModel, Query()], scraper: Scraper):
    return await scraper.get_data_from_page(
        start_page=model.start_page,
        end_page=model.end_page,
        region=model.region
    )
