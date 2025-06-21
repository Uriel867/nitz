import requests
from bs4 import BeautifulSoup
import cloudscraper

import time



class OverwatchScraper:
    # https://tracker.gg/overwatch/leaderboards/stats/all/Eliminations?page=100&plat=mouseKeyboard&gamemode=competitive
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
        
    async def get_data_from_page(self, start_page: int, end_page: int, platform: str, game_mode: str):
        # container to hold all the retrieved data
        data = []

        # query params
        params = {
            'plat': platform,
            'gamemode': game_mode
        }

        # writing to file block - TODO: change to reporting to DB
        with open('./users_quickplay.txt', 'a') as f:
            # traversing all pages and retrieving the data
            for page in range(start_page, end_page + 1):
                params['page'] = page
                # retrieving the data
                response = self.scraper.get(self.base_url, params=params)
                # only appending the data if request was successful
                if response.status_code == 200:
                    print(f'Appending data from page {page}...')
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
                        f.write(f'username: {data[-1]['username']}\ntag: {data[-1]['tag']}\n\n')
                else:
                    print(f'Request failed on page {page}...')
                    continue
            
            # sleeping to avoid IP block
            # time.sleep(1)

        return data
       

