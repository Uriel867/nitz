from pydantic import BaseModel,model_validator

class SummonerModel(BaseModel):
    summoner_name: str
    battle_tag: str
    puuid: str
    
    @model_validator(mode='after')
    def validate_summoner_name(self):
        if self.summoner_name is None:
            raise ValueError("Summoner name cannot be empty")
        
    @model_validator(mode='after')
    def validate_battle_tag(self):
        if self.battle_tag is None:
            raise ValueError("Battle tag cannot be empty")
        
        if not self.battle_tag.startswith('#'):
            raise ValueError("Battle tags must start with #")
        
    @model_validator(mode='after')
    def validate_puuid(self):
        if self.puuid is None:
            raise ValueError("Puuid cannot be empty")
    
class MatchModel(BaseModel):
    match_id: str
    
    @model_validator(mode='after')
    def validate_match_id(self):
        if self.match_id is None:
            raise ValueError("Match id cannot be empty")