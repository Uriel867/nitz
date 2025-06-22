from bs4 import BeautifulSoup
import cloudscraper
import asyncio

from .exceptions import HttpResponseException


class TrackerGGScraper:
    def __init__(self, base_url='https://tracker.gg/overwatch/leaderboards/stats/all/Eliminations'):
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
        
        
    async def get_data_from_page(self, start_page: int, end_page: int, platform: str, game_mode: str):
        # container to hold all the retrieved data
        data = []
        futures = []

        # query params
        params = {
            'plat': platform,
            'gamemode': game_mode
        }

        # traversing all pages and retrieving the data
        for page in range(start_page, end_page + 1):
            try:
                futures.append(
                    self._scrape_page(
                        page=page,
                        query_params=params
                    )
                )
            except HttpResponseException as e:
                break

        # awaiting all calls together
        texts = await asyncio.gather(*futures)

        for text in texts:
            text_data = self._parse_text(text)
            data.extend(text_data)

        return data
    
    async def _scrape_page(
            self, 
            page: int, 
            query_params: dict
        ):
        query_params['page'] = page
        
        return await self._request(url=self.base_url, params=query_params)
    
    async def _request(self, url, params):
        with self.scraper.get(url, params=params) as response:
            return response.text
        
    def _parse_text(self, text):
        data = []

        soup = BeautifulSoup(text, 'html.parser')
        # extracting usernames and battle tags values from the html response
        usernames = soup.find_all('span', class_=['trn-ign__username', 'fit-long-username'])
        tags = soup.find_all('span', class_='trn-ign__discriminator')

        # appending each username#tag to the data container and writing to file - TODO: change to reporting to DB
        for i in range(len(usernames)):
            data.append({
                'username': usernames[i].get_text(strip=True),
                'tag': tags[i].get_text(strip=True)
            })
        
        return data
