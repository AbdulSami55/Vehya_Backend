from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers.NewsFeed import newsfeed
from routers.Videos import videos
from routers.Users import users
from routers.FeaturedProducts import featuredProducts


app = FastAPI()
app.include_router(newsfeed.router)
app.include_router(videos.router)
app.include_router(featuredProducts.router)
app.include_router(users.router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/health')
def get_health():
    return {"status":"OK","code":200}

if __name__=='__main__':
    uvicorn.run(app=app,host='192.168.18.84',port=7000)