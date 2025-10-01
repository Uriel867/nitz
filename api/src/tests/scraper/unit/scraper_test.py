import pytest
from fastapi.testclient import TestClient

from main import app

# creating a single client as a generator to be used in testing
@pytest.fixture
def client():
    yield TestClient(app)

# creating several test cases with values for start_page, end_page and sub_region in tuples
# @pytest.mark.parametrize('start_page, end_page, sub_region', [
#     (1, 1, 'eune'),
#     (1, 1, 'euw')
# ])
# def test_scrape_endpoint(client: TestClient, start_page: int, end_page: int, sub_region: str):
#     query_params = {
#         'start_page': start_page,
#         'end_page': end_page,
#         'sub_region': sub_region
#     }
#     response = client.get('/scrape', params=query_params)
#
#     assert response.status_code == 200
#     assert len(response.json()) == 100

def test_health(client: TestClient):
    response = client.get('/health')
    assert response.status_code == 200
