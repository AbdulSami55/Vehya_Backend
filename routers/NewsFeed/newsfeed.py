from fastapi import APIRouter, Depends, HTTPException, UploadFile,File,status
from ..NewsFeed import schemas, crud
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/News_Feed",
    tags=["NewsFeed"],
)




@router.post("/create-news")
async def create_news(news:schemas.NewsFeed=Depends(), Image: UploadFile=File(...), db: Session = Depends(get_db)):
    try:
        upload_image = crud.upload_image_file(file=Image, news=news)
        News = schemas.CompleteNewsFeed(title=news.title, description=news.description, category=news.category, image=upload_image)
        return crud.addNews(db=db,news=News)
        
    except:
        
        raise HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.get('/get_news_by_ID')
async def get_news_by_id(NewsID:int, db:Session = Depends(get_db)):
    try:
        return crud.getNews(db=db, id=NewsID)

    except:
        raise HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.get('/Get-Article-By-Page-No')
async def get_news_article(PageNo:int,db:Session = Depends(get_db) ):
    return crud.getNewsArticle(db=db, PageNo=PageNo)