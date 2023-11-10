import json
import os
from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile,File,status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from ..NewsFeed import schemas, crud
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine, get_db
import shutil
from sqlalchemy import desc

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/News_Feed",
    tags=["NewsFeed"],
)



@router.post("/create-news")
async def create_news(Title: str = Form(...), 
    Section1: Optional[str] = Form(None),  
    Section2: Optional[str] = Form(None),  
    Section3: Optional[str] = Form(None),
    Section4: Optional[str] = Form(None),
    Category: str = Form(...),ShortDescription: str = Form(...), Image: UploadFile=File(...), db: Session = Depends(get_db)):
    try:
        description = {
            "Section1": Section1,
            "Section2": Section2,
            "Section3": Section3,
            "Section4": Section4,
        }
       
       
        upload_image = crud.upload_image_file_test(file=Image, Category=Category)
        News = schemas.CompleteNewsFeed(Title=Title, Description=description, ShortDescription=ShortDescription, Category=Category, Image=upload_image)
        return crud.addNews(db=db,news=News)
        
    except:
        raise HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @router.post("/create-news")
# async def create_news(news:schemas.NewsFeed=Depends(), Image: UploadFile=File(...), db: Session = Depends(get_db)):
#     try:
#         upload_image = crud.upload_image_file(file=Image, news=news)
#         description = crud.writeHTMLfile(data=news.Description)
#         News = schemas.CompleteNewsFeed(Title=news.Title, Description=description, ShortDescription=news.ShortDescription, Category=news.Category, Image=upload_image)
#         return crud.addNews(db=db,news=News)
        
#     except:
#         raise HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.get('/get_news_by_ID')
async def get_news_by_id(NewsID:int, db:Session = Depends(get_db)):
    try:
        return crud.getNews(db=db, id=NewsID)

    except:
        raise HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.get('/Get-Article-By-Page-No')
async def get_news_article(PageNo:int,db:Session = Depends(get_db) ):
    return crud.getNewsArticle(db=db, PageNo=PageNo)

@router.get('/Get-All-Articles')
async def get_news_article(db:Session = Depends(get_db) ):
    try:
        with db as session:
            columns = [models.NewsFeed.id, models.NewsFeed.Category, models.NewsFeed.Image, models.NewsFeed.ShortDescription,models.NewsFeed.Title]
            news = session.query(*columns).order_by(models.NewsFeed.id.desc()).all()
        if news:
            return news, {'TotalRows':len(news)}
        else:
            return {'Message':'No data exists'}
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    

@router.get('/Get-Article-Charging-Resiliency')
async def get_news_article_CR(db:Session = Depends(get_db) ):
    try:
        charging = db.query(models.NewsFeed).filter(models.NewsFeed.Category=='Charging').order_by(models.NewsFeed.id.desc()).limit(4).all()
        resiliency = db.query(models.NewsFeed).filter(models.NewsFeed.Category=='Resiliency').order_by(models.NewsFeed.id.desc()).limit(2).all()
        return{'Charging':charging,
               'Resiliency':resiliency}     
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.get('/Get-Article-ServicePRO')
async def get_servicePRO_article(PageNo:int,db:Session = Depends(get_db) ):
    return crud.getServicePROArticle(db=db, PageNo=PageNo)

@router.get('/Get-Article-Charging')
async def get_Charging_article(PageNo:int,db:Session = Depends(get_db) ):
    return crud.getChargingArticle(db=db, PageNo=PageNo)


# @router.put('/Update-Article')
# async def updateNewsArticle(Article:schemas.UpdateNewsFeed=Depends(),file:Optional[UploadFile]=None,db:Session = Depends(get_db) ):
#     # try:
#         article = db.query(models.NewsFeed).filter(models.NewsFeed.id==Article.Id).first()
#         if article:
#             if file is None:
                
#                 # new_folder_name = crud.change_image_folder_name(old_name=article.Category, new_name=Article.category)
#                 new_folder_name = f'Static/Files/NewsFeed/{Article.Category}'
#                 if os.path.exists(new_folder_name):
#                     if(Article.Category==article.Category):
#                         image_path=article.Image
#                     else:
#                         shutil.move(article.Image,f'{new_folder_name}/Images/') 
#                         image_path=f'{new_folder_name}/Images/{os.path.basename(article.Image)}'     
#                 else:
#                     os.makedirs(f'{new_folder_name}/Images')
#                     shutil.move(article.Image,f'{new_folder_name}/Images/')  
#                     image_path = f'{new_folder_name}/Images/{os.path.basename(article.Image)}'
#                 if(Article.Description==None):
#                     description = article.Description
#                 else:
#                     description = crud.writeHTMLfile(data=Article.Description)
#                     if isinstance(description,str):
#                         os.remove(article.Description)
#                     else:
#                         return HTTPException(detail='Could not update Article',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    
#                 image_file_name = os.path.basename(article.Image)
#                 new_image_path = f'{new_folder_name}/Images/{image_file_name}'
#                 updated_article = {
#                         "id": Article.Id,
#                         "Title":Article.Title,
#                         "Description":description,
#                         "ShortDescription":Article.ShortDescription,
#                         "Category": Article.Category,
#                         "Image": image_path # Keep the existing Image
                        
#                     }
#             else:
                
                
#                 # new_folder_name = f'Static/Files/NewsFeed/{Article.Category}'
#                 # if os.path.exists(new_folder_name):
#                 #     shutil.move(article.Image,f'{new_folder_name}/Images/')       
#                 # else:
#                 #     os.makedirs(f'{new_folder_name}/Images')
#                 # # new_folder_name = crud.change_image_folder_name(old_name=article.Category, new_name=Article.category)
#                 image_file = crud.upload_image_file(file=file,news=Article)
#                 os.remove(article.Image)
#                 if(Article.Description==None):
#                     description = article.Description
#                 else:
#                     description = crud.writeHTMLfile(data=Article.Description)
#                     if isinstance(description,str):
#                         os.remove(article.Description)
#                     else:
#                         return HTTPException(detail='Could not update Article',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)   
#                 if isinstance(image_file, str):
#                     updated_article = {
#                         "id": Article.Id,
#                         "Title":Article.Title,
#                         "Description":description,
#                         "ShortDescription":Article.ShortDescription,
#                         "Category": Article.Category,
#                         "Image": image_file 
#                     }
#                 else:
#                     return HTTPException(detail='An Error Occoured while uploading new Image file', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             UpdateArticle = db.query(models.NewsFeed).filter(models.NewsFeed.id==Article.Id)
#             UpdateArticle.update(updated_article)
#             db.commit()
#             return {'Message':'Successfully Updated Article'}
            
#         else:
#             return HTTPException(detail='News Article does not exist', status_code=status.HTTP_404_NOT_FOUND)

#     # except:
#     #     return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/Update-Article')
async def updateNewsArticle(Id:int=Form(...),Title: str = Form(...)
                            ,Section1: Optional[str] = Form(None),  
                            Section2: Optional[str] = Form(None),  
                            Section3: Optional[str] = Form(None),
                            Section4: Optional[str] = Form(None)
                            ,Category: str = Form(...),ShortDescription: str = Form(...),file:Optional[UploadFile]=None,db:Session = Depends(get_db) ):
    try:
        article = db.query(models.NewsFeed).filter(models.NewsFeed.id==Id).first()

        Description = {
            "Section1": Section1,
            "Section2": Section2,
            "Section3": Section3,
            "Section4": Section4,
        }
     
        if article:
            if file is None:
                # new_folder_name = crud.change_image_folder_name(old_name=article.Category, new_name=Article.category)
                new_folder_name = f'Static/Files/NewsFeed/{Category}'
                if os.path.exists(new_folder_name):
                    if(Category==article.Category):
                        image_path=article.Image
                    else:
                        shutil.move(article.Image,f'{new_folder_name}/Images/') 
                        image_path=f'{new_folder_name}/Images/{os.path.basename(article.Image)}'     
                else:
                    os.makedirs(f'{new_folder_name}/Images')
                    shutil.move(article.Image,f'{new_folder_name}/Images/')  
                    image_path = f'{new_folder_name}/Images/{os.path.basename(article.Image)}'
                if(Description==None):
                    description = article.Description
                else:
                    description = Description
                    # if isinstance(description,str):
                    #     os.remove(article.Description)
                    # else:
                    #     return HTTPException(detail='Could not update Article',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    
                image_file_name = os.path.basename(article.Image)
                new_image_path = f'{new_folder_name}/Images/{image_file_name}'
                updated_article = {
                        "id": Id,
                        "Title":Title,
                        "Description":description,
                        "ShortDescription":ShortDescription,
                        "Category": Category,
                        "Image": image_path # Keep the existing Image
                        
                    }
            else:
                # new_folder_name = f'Static/Files/NewsFeed/{Article.Category}'
                # if os.path.exists(new_folder_name):
                #     shutil.move(article.Image,f'{new_folder_name}/Images/')       
                # else:
                #     os.makedirs(f'{new_folder_name}/Images')
                # # new_folder_name = crud.change_image_folder_name(old_name=article.Category, new_name=Article.category)
                image_file = crud.upload_image_file_test(file=file,Category=Category)
                os.remove(article.Image)
                if(Description==None):
                    description = article.Description
                else:
                    description = Description
                    # if isinstance(description,str):
                    #     os.remove(article.Description)
                    # else:
                    #     return HTTPException(detail='Could not update Article',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)   
                if isinstance(image_file, str):
                    updated_article = {
                        "id": Id,
                        "Title":Title,
                        "Description":description,
                        "ShortDescription":ShortDescription,
                        "Category": Category,
                        "Image": image_file 
                    }
                else:
                    return HTTPException(detail='An Error Occoured while uploading new Image file', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            UpdateArticle = db.query(models.NewsFeed).filter(models.NewsFeed.id==Id)
            UpdateArticle.update(updated_article)
            db.commit()
            return {'Message':'Successfully Updated Article'}
            
        else:
            return HTTPException(detail='News Article does not exist', status_code=status.HTTP_404_NOT_FOUND)
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@router.delete('/Delete-News-Article')
async def deleteArticle(ArticleID:int, db:Session = Depends(get_db)):
    Article = db.query(models.NewsFeed).filter(models.NewsFeed.id==ArticleID)
    ArticleData= db.query(models.NewsFeed).filter(models.NewsFeed.id==ArticleID).first()
    if Article and ArticleData is not None :
        Article.delete(synchronize_session=False)
        # os.remove(ArticleData.Description)
        os.remove(ArticleData.Image)
        db.commit()
        return {'Message':'Article Deleted Successfully'}
    else:
        return HTTPException(detail='No News Article Found',status_code=status.HTTP_404_NOT_FOUND)  


@router.get('/Send-File-Response')
async def SendImageFile(FilePath:str ):
    # try:
        return FileResponse(FilePath)
        # if os.path.isfile(FilePath):
            # return FileResponse(FilePath, media_type="application/octet-stream")
        # else:
        #     return HTTPException(detail='File Path Invalid',status_code=status.HTTP_404_NOT_FOUND)

    # except:
    #     return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.get('/Send-HTML-File-Response')
async def SendHTMLfile(FilePath:str):
    try:
        with open(FilePath, "r", encoding="utf-8") as file:
            html_content = file.read()
            return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)    