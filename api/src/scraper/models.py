from pydantic import BaseModel, Field, model_validator
from enum import StrEnum


class LeagueOfGraphsSubRegion(StrEnum):
    BR = 'br'
    EUNE = 'eune'
    EUW = 'euw'
    JP = 'jp'
    KR = 'kr'
    LAN = 'lan'
    LAS = 'las'
    ME = 'me'
    NA = 'na'
    OCE = 'oce'
    RU = 'ru'
    SEA = 'sea'
    TR = 'tr'
    TW = 'tw'
    VN = 'vn'

class LeagueOfGraphsModel(BaseModel):
    # page number must be between 1 and 9999
    start_page: int = Field(1, ge=1, le=9999)
    end_page: int = Field(1, ge=1, le=9999)
    sub_region: LeagueOfGraphsSubRegion = Field(LeagueOfGraphsSubRegion.EUW)

    @model_validator(mode='after')
    def validate_page_range(self) -> int:
        start_page = self.start_page
        end_page = self.end_page
        if start_page > end_page:
            raise ValueError(f'end_page must satisfy end_page <= start_page, but instead got start_page = {start_page}, end_page = {end_page}')
        return self
    
