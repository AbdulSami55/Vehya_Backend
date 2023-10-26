from pydantic import BaseModel

class Video(BaseModel):
    title:str
    description:str
    category:str
    lat:float
    long:float
    location:str

class CompleteVideo(Video):
    video:str
    