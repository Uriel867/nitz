from fastapi import APIRouter, Query, Depends
from typing import Annotated
from sqlalchemy import Engine, text

from .service import LeagueOfGraphsScraperService
from models.models import LeagueOfGraphsModel

from di.dependencies import provide_scraper_service, provide_postgres_engine


router = APIRouter(
    prefix='/scrape'
)

# defining an annotated type to reuse in multiple endpoints
Scraper = Annotated[LeagueOfGraphsScraperService, Depends(provide_scraper_service)]

@router.get('')
async def scrape_data(model: Annotated[LeagueOfGraphsModel, Query()], scraper: Scraper):
    return await scraper.scrape_pages(
        start_page=model.start_page,
        end_page=model.end_page,
        region=model.region
    )
