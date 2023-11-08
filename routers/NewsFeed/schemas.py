from typing import Optional,Dict
from pydantic import BaseModel



    
class NewsFeed(BaseModel):
    Title:str
    Description: Dict[str, Optional[str]]
    ShortDescription:str
    Category:str

class CompleteNewsFeed(NewsFeed):
    Image:str




class UpdateNewsFeed(BaseModel):
    Id:int
    Title:str
    Description:Dict[str, Optional[str]]
    ShortDescription:str
    Category:str