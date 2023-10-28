from fastapi import APIRouter, Depends, HTTPException, UploadFile,File,status
from fastapi.responses import FileResponse
from ..Videos import schemas, crud
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/Videos",
    tags=["Videos"],
)


@router.post("/Add-Video")
async def addVideo(video:schemas.CompleteVideo=Depends(), db: Session = Depends(get_db)):
    try:
        
        
        Video = schemas.CompleteVideo(Title=video.Title, Description=video.Description, Category=video.Category, Video=video.Video,
                                      Lat=video.Lat, Long=video.Long, Location=video.Location)
        return crud.addVideo(db=db,video=Video)
        
    except:
        
        raise HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get('/Get-Video-MetaData')
async def getVideoMetadata(VideoId:int,db:Session= Depends(get_db)):
    try:
        video = db.query(models.Videos).filter(models.Videos.id==VideoId).first()
        if video:
            return{
                'Title':video.Title,
                'Description':video.Description,
                'Category':video.Category,
                'Video':video.Video,
                'Lat':video.Lat,
                'Long':video.Long,
                'Location':video.Location
            }
        else:
            return {'Message':'No such data exists in database'}
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
@router.get('/Get-Map-Videos')
async def getMapVideos(db:Session= Depends(get_db)):
    try:
        Videos = db.query(models.Videos).offset(0).limit(100000).all()
        VideosList=[]
        for Video in Videos:
            singleVid = {
                            'id': Video.id,
                            'position': {
                                    'lat': Video.Lat, 
                                    'lng': Video.Long, 
                                         },
                            'UserDetail': {
                                            'Category':Video.Category,
                                            'VideoLink':Video.Video,
                                            'VideoTitle':Video.Title,
                                            'VideoDescription':Video.Description
                                            }
                        }
            VideosList.append(singleVid)
        return VideosList

    except:
        return HTTPException(detail='Something went wrong',status_code=status.WS_1011_INTERNAL_ERROR) 

@router.put('/Update-Video')
async def UpdateVideo(video:schemas.UpdateVideo,db:Session= Depends(get_db)):
    try:
        update_video={  "id": video.Id,
                        "Title":video.Title,
                        "Description":video.Description,
                        "Category": video.Category,
                        "Video":video.Video,
                        "Lat":video.Lat,
                        "Long":video.Long,
                        "Location":video.Location}
        UpdatedVideo = db.query(models.Videos).filter(models.Videos.id==video.Id)
        UpdatedVideo.update(update_video)
        db.commit()
        return {'Message':'Successfully Updated Article'}
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete('/Delete-Video')
async def DeleteVideo(VideoId:int,db:Session= Depends(get_db) ):
    try:
        return crud.deleteVideo(db=db, Id=VideoId)
    except:
        return HTTPException(detail='Something went wrong', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @router.get('/Get-Video-Stream')
# async def getVideoStreamResponse(VideoId:int,db:Session= Depends(get_db)):
#     try:
#         video = db.query(models.Videos).filter(models.Videos.id==VideoId).first()
#         if video:
#             return crud.getVideoStream(video.Video)
#         else:
#             return {'Message':'No such data exists in database'}
#     except:
#         return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)