import pytest
from fastapi.testclient import TestClient

from main import app

@pytest.fixture
def client():
    yield TestClient(app)

@pytest.mark.parametrize('start_page, end_page, region', [
    (1, 1, 'eune'),
    (1, 1, 'euw')
])
def test_scrape_endpoint(client: TestClient, start_page: int, end_page: int, region: str):
    query_params = {
        'start_page': start_page,
        'end_page': end_page,
        'region': region
    }
    response = client.get('/scrape', params=query_params)

    assert response.status_code == 200
    assert len(response.json()) == 100
