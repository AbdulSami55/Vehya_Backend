from pydantic import BaseModel

class FeaturedProduct(BaseModel):
    ProductID:str
    Category:str