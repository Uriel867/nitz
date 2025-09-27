from fastapi import APIRouter, Query, Depends
from typing import Annotated

from scraper.service import ScraperService
from scraper.models import LeagueOfGraphsModel

from di.dependencies import provide_scraper_service


router = APIRouter(
    prefix='/scrape'
)

# defining an annotated type to reuse in multiple endpoints
Scraper = Annotated[ScraperService, Depends(provide_scraper_service)]

@router.get('')
async def scrape_data(model: Annotated[LeagueOfGraphsModel, Query()], scraper: Scraper):
    return await scraper.scrape_pages(
        start_page=model.start_page,
        end_page=model.end_page,
        sub_region=model.sub_region
    )
