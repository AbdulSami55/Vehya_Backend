from pydantic import BaseModel

class Video(BaseModel):
    Title:str
    Description:str
    Category:str
    Lat:float
    Long:float
    Location:str

class CompleteVideo(Video):
    Video:str
    
class UpdateVideo(CompleteVideo):
    Id:int    
