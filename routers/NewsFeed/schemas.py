from typing import Optional
from pydantic import BaseModel

class NewsFeed(BaseModel):
    Title:str
    Description:str
    Category:str

class CompleteNewsFeed(NewsFeed):
    Image:str

class UpdateNewsFeed(NewsFeed):
    Id:int
    # image:Optional[str]