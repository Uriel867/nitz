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

@router.get('/lol')
async def get_puuid_by_summoner_name_and_tag(
    summoner_name: str, 
    summoner_tag: str, 
    table_name: str, 
    engine: Engine = Depends(provide_postgres_engine)
):
    import requests
    import os
    import json

    headers = {
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": os.environ['RIOT_GAMES_API_KEY']
    }
    
    url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{summoner_tag}'

    response = requests.get(url=url, headers=headers)

    json_data = json.loads(response.content)

    with engine.begin() as conn:
        conn.execute(text(f'CREATE TABLE {table_name} (x int, y int)'))
        conn.execute(
            text(f'INSERT INTO {table_name} (x, y) VALUES (:x, :y)'),
            [{'x': 1, 'y': 16}, {'x': 13, 'y': 27}]
        )

        result = conn.execute(text(f'SELECT x AS ziv, y AS lazarov FROM {table_name}'))
        for row in result:
            print(f'x: {row.ziv}, y: {row.lazarov}')
    
    return json_data
