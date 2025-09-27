from typing import List, Dict
from bs4 import BeautifulSoup
from .utils import SUB_REGION_TO_REGION
import cloudscraper
import asyncio

from .exceptions import HttpResponseException


class ScraperService:
    def __init__(self, base_url='https://www.leagueofgraphs.com/rankings/summoners'):
        super().__init__()

        self.base_url = base_url
        self.scraper = cloudscraper.create_scraper(
            disableCloudflareV1=True,
            browser={
                'browser': 'firefox',
                'platform': 'linux',
                'mobile': False
            }
        )
        
        
    async def scrape_pages(self, start_page: int, end_page: int, sub_region: str) -> List[Dict[str, str]]:
        # container to hold all the retrieved data
        data = []
        futures = []

        # traversing all pages and retrieving the data
        for page in range(start_page, end_page + 1):
            try:
                futures.append(self._scrape_page(page=page, sub_region=sub_region))
            except HttpResponseException as e:
                break

        # awaiting all calls together
        texts = await asyncio.gather(*futures)

        for text in texts:
            text_data = self._parse_text(text, sub_region=sub_region)
            data.extend(text_data)

        return data
    
    async def _scrape_page(self, page: int, sub_region: str) -> str:
        url = f'{self.base_url}/{sub_region}/page-{page}'
        return await self._request(url=url)
    
    async def _request(self, url: str) -> str:
        with self.scraper.get(url) as response:
            return response.text
        
    def _parse_text(self, text: str, sub_region: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(text, 'html.parser')
        # extracting usernames and battle tags values from the html response
        full_summoners_names = soup.find_all('span', class_=['name'])
        # appending each game_name#tag_line to the data container
        data = []
        for i in range(len(full_summoners_names)):
            full_summoner_name = full_summoners_names[i].get_text(strip=True)
            game_name, tag_line = full_summoner_name.split('#')
            data.append({
                'full_summoner_name': full_summoner_name,
                'game_name': game_name,
                'tag_line': tag_line,
                'sub_region': sub_region,
                'region': SUB_REGION_TO_REGION[sub_region]
            })
        
        return data
