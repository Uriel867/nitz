from pydantic import BaseModel, model_validator

class SummonerModel(BaseModel):
    game_name: str
    tag_line: str
    
    @model_validator(mode='after')
    def validate_game_name(self):
        if self.game_name is None:
            raise ValueError("Summoner name cannot be empty")
        return self
        
    @model_validator(mode='after')
    def validate_tag_line(self):
        if self.tag_line is None:
            raise ValueError("tag_line cannot be empty")

        return self
