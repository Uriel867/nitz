from pydantic import BaseModel, Field, model_validator
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

    @model_validator(mode='after')
    def validate_page_range(self) -> int:
        start_page = self.start_page
        end_page = self.end_page
        if start_page > end_page:
            raise ValueError(f'end_page must satisfy end_page <= start_page, but instead got start_page = {start_page}, end_page = {end_page}')
        return self
    
