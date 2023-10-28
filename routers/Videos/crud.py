from fastapi import HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from ..Videos import schemas
import models
import datetime
import os
from fastapi import status
from sqlalchemy.orm import Session
import shutil

# def upload_thumbnail(file,video:schemas.Video):
#     file_extension = file.filename.split(".")[-1]
#     allowed_extensions = ["jpg", "jpeg", "png"]
#     if file_extension.lower() in allowed_extensions:
        
    
#         try:
#             contents = file.file.read()
#             current_time=datetime.datetime.now()
#             current_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
#             file_path=f'Static/Files/Video/{video.category}/Thumbnail/Images'
#             if not os.path.exists(file_path):
#                 os.makedirs(file_path)
#             final_file_path=f'{file_path}/{current_time}__{file.filename}'
#             with open(final_file_path, 'wb') as f:
#                 f.write(contents)

#         except Exception:
#             os.remove(final_file_path)
#             return HTTPException(detail="There was an error uploading the file",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         finally:
#             file.file.close()
#         return final_file_path
#     else:
#         return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="File Type Invalid")
    
# def upload_video(file,video:schemas.Video):
#     # Check if the uploaded file is a video (you can implement more detailed checks)
#     if file.content_type.startswith("video/"):
#        try: 
#             # Create a directory to store uploaded videos (if it doesn't exist)
#             current_time=datetime.datetime.now()
#             current_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
#             path = f'Static/Files/Video/{video.category}/Video'
#             if not os.path.exists(path):
#                 os.makedirs(path)
#             final_path = f"{path}/{current_time}__{file.filename}"

#             # Save the file to the "uploaded_videos" directory
#             with open(final_path, "wb") as f:
#                 shutil.copyfileobj(file.file, f) 
#             return final_path
#        except:  
#             return HTTPException(detail="There was an error uploading the file",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
         
#     return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="File Type Invalid") 



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

  