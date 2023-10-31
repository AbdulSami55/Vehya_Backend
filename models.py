from sqlalchemy import  Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    Email = Column(String)
    Password=Column(String)



class NewsFeed(Base):
    __tablename__ = "news_feed"
    id = Column(Integer, primary_key=True, index=True)
    Title=Column(String)
    Description=Column(String)
    Category=Column(String)
    Image=Column(String)


class Videos(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    Title=Column(String)
    Description=Column(String)
    Category=Column(String)
    Video=Column(String)
    Lat = Column(Float, default=0.0)
    Long = Column(Float, default=0.0)
    Location=Column(String)

class FeaturedProducts(Base):
    __tablename__ = "featured_products"
    id = Column(Integer, primary_key=True, index=True)
    ProductID = Column(String)
    Category = Column(String)
