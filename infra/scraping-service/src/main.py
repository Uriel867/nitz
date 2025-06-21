from typing import Union
from enum import Enum

from scraper.scraper import OverwatchScraper
from models.scraping_models import TrackerGGModel

from fastapi import FastAPI

# to be used with categorical values when calling an endpoint
class ModelName(str, Enum):
    alex_net = 'AlexNet'
    res_net = 'ResNet'

app = FastAPI()

@app.get('/')
async def hello_world():
    return { 'hello': 'world' }

@app.post('/scrape')
async def read_item(tracker_model: TrackerGGModel):
    print(tracker_model)
    scraper = OverwatchScraper()
    return await scraper.get_data_from_page(
        start_page=tracker_model.start_page,
        end_page=tracker_model.end_page, 
        platform=tracker_model.platform.value, 
        game_mode=tracker_model.game_mode.value
    )

@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name is ModelName.alex_net:
        return { 'model_name': model_name, 'message': 'AlexNet is ancient...' }
    
    if model_name.value == 'resnet' or model_name.value == ModelName.res_net.value:
        return { 'model_name': model_name, 'message': 'ResNet is a bit more modern...' }
    
    return { 'model_name': model_name, 'message': 'Non existing model that we know of...' }
