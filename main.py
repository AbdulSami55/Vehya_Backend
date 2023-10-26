from fastapi import Depends, FastAPI, HTTPException, Response,status,Header
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, StreamingResponse, JSONResponse
import uvicorn
from database import SessionLocal, get_db
from fastapi.middleware.cors import CORSMiddleware
from routers.NewsFeed import newsfeed
from routers.Videos import videos
from routers.Users import users
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

