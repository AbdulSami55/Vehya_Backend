from pydantic import BaseModel

class NewsFeed(BaseModel):
    title:str
    description:str
    category:str

class CompleteNewsFeed(NewsFeed):
    image:str

