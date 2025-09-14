import pytest

import requests

def scrape(start_page: int, end_page: int, region: str):
    url = 'http://localhost:8080/scrape'
    query_params = {
        'start_page': start_page,
        'end_page': end_page,
        'region': region,
    }
    response = requests.get(url=url, params=query_params)
    return response

def retrieve_puuid(tag_line: str, game_name: str, region: str):
    response = requests.get(f'http://localhost:8080/account/{region}/{game_name}/{tag_line}')
    return response

def test_scrape_endpoint():
    response = scrape(start_page=1, end_page=1, region='eune')
    assert response.status_code == 200
    assert len(response.json()) == 100

def test_puuid_retrieval():
    response = retrieve_puuid(game_name='ice cubes', tag_line='eune', region='europe')
    json = response.json()

    assert response.status_code == 200
    assert 'puuid' in json.keys() \
        and 'tagLine' in json.keys() \
        and 'gameName' in json.keys()
