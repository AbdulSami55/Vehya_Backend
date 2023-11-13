import math
from fastapi import HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from ..Videos import schemas
import models
from fastapi import status
from sqlalchemy.orm import Session

def getVideosByPageNumber(db:Session, PageNo:int,page_description:str):
    end_index = PageNo*3
    start_index = (end_index-3)
    if page_description=='home':
        total_rows =  db.query(models.Videos).filter(models.Videos.Category!='Charging').count()
    else:
        total_rows =  db.query(models.Videos).filter(models.Videos.Category=='Service PROs').count()
    total_pages = (total_rows / 3 )
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
    if page_description=='home':
        videos = db.query(models.Videos).filter(models.Videos.Category!='Charging').order_by(models.Videos.id.desc()).slice(start=start_index, stop=end_index).all()
    else:
        videos = db.query(models.Videos).filter(models.Videos.Category=='Service PROs').order_by(models.Videos.id.desc()).slice(start=start_index, stop=end_index).all()
    key=''
    if(len(videos)==3):
        key='continue'
    else:
        key='last'        
    return {'PageNo':PageNo,
            'Videos':videos,
            'Key':key,
            'TotalPages':total_pages_rounded,
            'TotalData':total_rows
            }    


def addVideo(db:Session, video:schemas.CompleteVideo):
    try:
        Video= models.Videos(Title=video.Title, Description=video.Description, Category=video.Category,  
                              Video=video.Video, Lat=video.Lat, Long=video.Long, Location=video.Location )
        db.add(Video)
        db.commit()
        db.refresh(Video)
        return "Data Uploaded"
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def deleteVideo(db:Session, Id:int):
    try:
        Video= db.query(models.Videos).filter(models.Videos.id==Id)
        Video.delete(synchronize_session=False)
        db.commit()
        return "Video Deleted Successfully"
    except:
        return HTTPException(detail="Something Went Wrong",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def getVideoStream(path:str):
#     video_path = path  # Replace with the actual path to your video file
    
#     if not os.path.exists(video_path):
#         return JSONResponse(content={"error": "Video not found"}, status_code=404)
    
#     def generate():
#         with open(video_path, "rb") as video_file:
#             while True:
#                 video_chunk = video_file.read(1024 * 1024)  # Read 1MB at a time
#                 if not video_chunk:
#                     break
#                 yield video_chunk

#     return StreamingResponse(content=generate(), media_type="video/mp4")

  