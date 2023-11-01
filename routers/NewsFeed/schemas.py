from typing import Optional
from pydantic import BaseModel

class NewsFeed(BaseModel):
    Title:str
    Description:str
    ShortDescription:str
    Category:str

class CompleteNewsFeed(NewsFeed):
    Image:str

class UpdateNewsFeed(BaseModel):
    Id:int
    Title:str
    Description:Optional[str]
    ShortDescription:str
    Category:str