from pydantic import BaseModel
from enum import Enum

class TrackerGGPlatform(str, Enum):
    pc = 'mouseKeyboard'
    console = 'controller'

class TrackerGGGameMode(str, Enum):
    competitive = 'competitive'
    quick_play = 'quickPlay'

class TrackerGGModel(BaseModel):
    start_page: int = 1
    end_page: int = 1
    platform: TrackerGGPlatform = TrackerGGPlatform.pc.value
    game_mode: TrackerGGGameMode = TrackerGGGameMode.competitive.value

