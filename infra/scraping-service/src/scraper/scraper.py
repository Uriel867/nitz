from bs4 import BeautifulSoup
import cloudscraper
from io import TextIOWrapper
import asyncio
import aiohttp

from .exceptions import HttpResponseException


class TrackerGGScraper():
    def __init__(self, base_url='https://tracker.gg/overwatch/leaderboards/stats/all/Eliminations'):
        self.base_url = base_url
        self.scraper = cloudscraper.create_scraper(
            disableCloudflareV1=True,
            browser={
                'browser': 'firefox',
                'platform': 'linux',
                'mobile': False
            }
        )

        # self.session = aiohttp.ClientSession()

    async def __del__(self):
        await self.session.close()
        
    async def get_data_from_page(self, start_page: int, end_page: int, platform: str, game_mode: str, write_to_file: bool):
        # container to hold all the retrieved data
        data = []
        futures = []

        # query params
        params = {
            'plat': platform,
            'gamemode': game_mode
        }

        if write_to_file:
            # writing to file block - TODO: change to reporting to DB
            with open('./users_test.txt', 'a') as f:
                # traversing all pages and retrieving the data
                for page in range(start_page, end_page + 1):
                    try:
                        futures.append(
                            self._scrape_page(
                                page=page,
                                query_params=params,
                                data=data,
                                write_to_file=write_to_file,
                                file=f
                            )
                        )
                    except HttpResponseException as e:
                        break
                # sleeping to avoid IP block
                # time.sleep(1)
        else:
            # not writing to file
            for page in range(start_page, end_page + 1):
                try:
                    futures.append(
                        self._scrape_page(
                            page=page,
                            query_params=params,
                            data=data,
                            write_to_file=write_to_file
                        )
                    )
                except HttpResponseException as e:
                    break
        # awaiting all calls together
        await asyncio.gather(*futures)

        return data[:100]
    
    async def _scrape_page(
            self, 
            page: int, 
            query_params: dict, 
            data: list, 
            write_to_file: bool, 
            file: TextIOWrapper=None
        ):
        query_params['page'] = page
        try:
            # retrieving the data
            response = self.scraper.get(self.base_url, params=query_params)
        except Exception:
            raise HttpResponseException(f'Page {page} couldn\'t be scraped! Please check network configurations.')
        # only appending the data if request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # extracting usernames and battle tags values from the html response
            usernames = soup.find_all('span', class_=['trn-ign__username', 'fit-long-username'])
            tags = soup.find_all('span', class_='trn-ign__discriminator')

            # appending each username#tag to the data container and writing to file - TODO: change to reporting to DB
            for i in range(len(usernames)):
                data.append({
                    'username': usernames[i].get_text(strip=True),
                    'tag': tags[i].get_text(strip=True)
                })
                if write_to_file:
                    file.write(f'username: {data[-1]['username']}\ntag: {data[-1]['tag']}\n\n')
        else:
            raise Exception(f'Page {page} couldn\'t be scraped!')

       

