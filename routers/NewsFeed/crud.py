from fastapi import HTTPException
from ..NewsFeed import schemas
import models
import datetime
import os
from fastapi import status
from sqlalchemy.orm import Session
import math

def upload_image_file(file,news:schemas.NewsFeed):
    file_extension = file.filename.split(".")[-1]
    allowed_extensions = ["jpg", "jpeg", "png"]
    if file_extension.lower() in allowed_extensions:
        
    
        try:
            contents = file.file.read()
            current_time=datetime.datetime.now()
            current_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
            file_path=f'Static/Files/NewsFeed/{news.Category}/Images'
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

def change_image_folder_name(old_name:str, new_name:str):
    #_____________________Renaming Directory according to new Username___________________________________*
    path = 'Static/Files/NewsFeed/'
    try:
        for root, dirs, files in os.walk(path):
            for dir_name in dirs:
                if dir_name == old_name:
                    old_path = os.path.join(root, dir_name)
                    new_path = os.path.join(root, new_name)

                    os.rename(old_path, new_path)
                    return new_path
    except Exception as e:
        print(f"An error occurred: {e}")

def save_updated_logo_file(new_path:str, file):  
     #_____________________Saving New Logo File to Renamed Folder___________________________________*
    file_extension = file.filename.split(".")[-1]
    allowed_extensions = ["jpg", "jpeg", "png"]
    if file_extension.lower() not in allowed_extensions:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="File Type Invalid") 
    try:
        contents = file.file.read()
        file_path = f'{new_path}/Images/{file.filename}'
        with open(file_path, 'wb') as f:
            f.write(contents)
            f.close()
        return file_path
    except:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something Went Wrong")


def addNews(db:Session, news:schemas.CompleteNewsFeed):
    try:
        News= models.NewsFeed(Title=news.Title, Description=news.Description, Category=news.Category, Image=news.Image)
        db.add(News)
        db.commit()
        db.refresh(News)
        return "Data Uploaded"
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def writeHTMLfile(data:str):
    # try:
        path='Static/Files/NewsFeed/HTML_Files'
        current_time=datetime.datetime.now()
        current_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f"{path}/{current_time}_.html"
        with open(file_path, "w") as file:
            file.write(data)
        return file_path
    # except:
    #     return HTTPException(detail='Something went wrong while writing HTML content',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    total_pages = (total_rows / 6 )
    if total_pages % 1 > 0:
        # Round up to the next whole number
        total_pages_rounded = math.ceil(total_pages)
    else:
        # It's already a whole number
        total_pages_rounded = int(total_pages)
    Pages=list(range(1, int(total_pages)+2 ))
    if (end_index>total_rows):
        end_index=total_rows
    if(start_index>end_index):
        return HTTPException(detail='Page Does Not Exist', status_code=status.HTTP_404_NOT_FOUND)    
    NewsArticles=[]
    articles = db.query(models.NewsFeed).slice(start=start_index, stop=end_index).all()
    for article in articles:
        NewsArticles.append(article)
    # length=len(NewsArticles)    
    # print(length)
    key=''
    if(len(NewsArticles)==6):
        key='continue'
    else:
        key='last'        
    return {'PageNo':PageNo,
            'NewsArticles':NewsArticles,
            'Key':key,
            'TotalPages':total_pages_rounded,
            'TotalData':total_rows
            }    


def getServicePROArticle(db:Session, PageNo:int):
    end_index = PageNo*6
    start_index = (end_index-6)
    total_rows = db.query(models.NewsFeed).filter(models.NewsFeed.Category=='Service PROs').count()
    total_pages = (total_rows / 6 )
    if total_pages % 1 > 0:
        # Round up to the next whole number
        total_pages_rounded = math.ceil(total_pages)
    else:
        # It's already a whole number
        total_pages_rounded = int(total_pages)

    Pages=list(range(1, int(total_pages)+1 ))
    if (end_index>total_rows):
        end_index=total_rows
    if(start_index>end_index):
        return HTTPException(detail='Page Does Not Exist', status_code=status.HTTP_404_NOT_FOUND)    
    NewsArticles=[]
    articles = db.query(models.NewsFeed).filter(models.NewsFeed.Category=='Service PROs').slice(start=start_index, stop=end_index).all()
    for article in articles:
        NewsArticles.append(article)
    # length=len(NewsArticles)    
    # print(length)
    key=''
    if(len(NewsArticles)==6):
        key='continue'
    else:
        key='last'        
    return {'PageNo':PageNo,
            'NewsArticles':NewsArticles,
            # 'Key':key,
            'TotalPages':total_pages_rounded,
            'TotalRows':total_rows
            }    

def getChargingArticle(db:Session, PageNo:int):
    end_index = PageNo*6
    start_index = (end_index-6)
    total_rows = db.query(models.NewsFeed).filter(models.NewsFeed.Category=='Charging').count()
    total_pages = (total_rows / 6 )
    Pages=list(range(1, int(total_pages)+1 ))
    if (end_index>total_rows):
        end_index=total_rows
    if(start_index>end_index):
        return HTTPException(detail='Page Does Not Exist', status_code=status.HTTP_404_NOT_FOUND)    
    NewsArticles=[]
    articles = db.query(models.NewsFeed).filter(models.NewsFeed.Category=='Charging').slice(start=start_index, stop=end_index).all()
    for article in articles:
        NewsArticles.append(article)
    # length=len(NewsArticles)    
    # print(length)
    key=''
    if(len(NewsArticles)==6):
        key='continue'
    else:
        key='last'        
    return {'PageNo':PageNo,
            'NewsArticles':NewsArticles,
            # 'Key':key,
            'TotalPages':int(total_pages),
            'Pages':Pages
            }    
    