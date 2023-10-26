from fastapi import HTTPException
from ..NewsFeed import schemas
import models
import datetime
import os
from fastapi import status
from sqlalchemy.orm import Session

def upload_image_file(file,news:schemas.NewsFeed):
    file_extension = file.filename.split(".")[-1]
    allowed_extensions = ["jpg", "jpeg", "png"]
    if file_extension.lower() in allowed_extensions:
        
    
        try:
            contents = file.file.read()
            current_time=datetime.datetime.now()
            current_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
            file_path=f'Static/Files/NewsFeed/{news.category}/Images'
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            final_file_path=f'{file_path}/{current_time}__{file.filename}'
            with open(final_file_path, 'wb') as f:
                f.write(contents)

        except Exception:
            os.remove(final_file_path)
            return HTTPException(detail="There was an error uploading the file",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            file.file.close()
        return final_file_path
    else:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="File Type Invalid")


def addNews(db:Session, news:schemas.CompleteNewsFeed):
    try:
        News= models.NewsFeed(Title=news.title, Description=news.description, Category=news.category, Image=news.image)
        db.add(News)
        db.commit()
        db.refresh(News)
        return "Data Uploaded"
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def getNews(db:Session, id:int):
    try:
        news = db.query(models.NewsFeed).filter(models.NewsFeed.id==id).first()
        if news:
            return{
                'Title':news.Title,
                'Description':news.Description,
                'Category':news.Category,
                'Image':news.Image
            }
        else:
            return {'Message':'No such data exists in database'}
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    

def getNewsArticle(db:Session, PageNo:int):
    end_index = PageNo*6
    start_index = (end_index-6)
    total_rows = db.query(models.NewsFeed).count()
    if (end_index>total_rows):
        end_index=total_rows
    if(start_index>end_index):
        return HTTPException(detail='Page Does Not Exist', status_code=status.HTTP_404_NOT_FOUND)    
    NewsArticles=[]
    articles = db.query(models.NewsFeed).slice(start=start_index, stop=end_index).all()
    for article in articles:
        NewsArticles.append(article)
    return {'Page No':PageNo,
            'News Articles':NewsArticles}    
    