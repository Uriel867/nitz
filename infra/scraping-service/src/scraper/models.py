from pydantic import BaseModel, Field
from enum import StrEnum

class TrackerGGPlatform(StrEnum):
    pc = 'mouseKeyboard'
    console = 'controller'

class TrackerGGGameMode(StrEnum):
    competitive = 'competitive'
    quick_play = 'quickPlay'

class TrackerGGModel(BaseModel):
    # page number must be between 1 and 9999
    start_page: int = Field(1, ge=1, le=9999)
    end_page: int = Field(1, ge=1, le=9999)
    platform: TrackerGGPlatform = Field(TrackerGGPlatform.pc)
    game_mode: TrackerGGGameMode = Field(TrackerGGGameMode.competitive)
