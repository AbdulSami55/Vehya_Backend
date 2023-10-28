import warnings
from fastapi import Depends, FastAPI, HTTPException, Response,status,Header
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, StreamingResponse, JSONResponse
import uvicorn
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from fastapi.middleware.cors import CORSMiddleware
from routers.NewsFeed import newsfeed
from routers.Videos import videos
from routers.Users import users
from pathlib import Path
import os
import cv2
app = FastAPI()
app.include_router(newsfeed.router)
app.include_router(videos.router)
app.include_router(users.router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/video")
# def stream_video():
#     video_path = 'Static/Files/Video/Travel & Nature/Video/2023-10-24_18-31-18__result_compressed.mp4'
#     return FileResponse(video_path, media_type="video/mp4")



# def iterfile():
#     video_path=f'Static\Files\Video\Travel & Nature\Video\2023-10-24_18-31-18__result_compressed.mp4'
#     outputFrame = cv2.VideoCapture(video_path)
#     while True:
#         status,img= outputFrame.read()
#         if status==False:
#             break
#         (flag, encodedImage) = cv2.imencode(".jpg", img)
#         if not flag:
#             continue
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
#                bytearray(encodedImage) + b'\r\n')
# @app.get('/video')
# def getvideo():
#     return StreamingResponse(iterfile(), media_type="multipart/x-mixed-replace;boundary=frame")






# CHUNK_SIZE=50*50
# @app.get("/video")
# async def video_endpoint(range: str = Header(None),path:str=None):
#     video_path = Path("Static/Files/Video/Food & Drink/Video/2023-10-24_18-42-53__SaveInsta.App - 3122528822300418910.mp4")
#     if range==None:
#         range = "bytes=0-"
#     start, end = range.replace("bytes=", "").split("-")
#     start = int(start)
#     end = int(end) if end else start + CHUNK_SIZE
#     print(range)
#     with open(video_path, "rb") as video:
#         video.seek(start)
#         data = video.read(end - start)
#         filesize = str(video_path.stat().st_size)
#         headers = {
#             "content-type": "video/mp4",
#             "content-encoding": "identity",
#             'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
#             'Accept-Ranges': 'bytes',
#             "content-length"  : filesize,
#             "access-control-expose-headers": (
#             "content-type, accept-ranges, content-length, "
#             "content-range, content-encoding"
#         ),
#         }
#         warnings.filterwarnings('ignore')
#         return Response(data, status_code=206, headers=headers, media_type="video/mp4")


if __name__=='__main__':
    uvicorn.run(app=app,host='192.168.18.106',port=7000)
