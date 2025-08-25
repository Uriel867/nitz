from pydantic import BaseModel,model_validator

class SummonerModel(BaseModel):
    summoner_name: str
    tag_line: str
    
    @model_validator(mode='after')
    def validate_summoner_name(self):
        if self.summoner_name is None:
            raise ValueError("Summoner name cannot be empty")
        return self
        
    @model_validator(mode='after')
    def validate_tag_line(self):
        if self.tag_line is None:
            raise ValueError("tag_line cannot be empty")
        
        if not self.tag_line.startswith('#'):
            raise ValueError("tag_line must start with #")

        return self