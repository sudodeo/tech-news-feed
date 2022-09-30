from fastapi import FastAPI
from .routers import news
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    endpoints = {"combined news": "/news", "cnet": "/news/cnet", "mashable": "/news/mashable",
                 "medium": "/news/medium", "the next web": "/news/tnw"}
    return {'Tech News': 'Get top trending news via this API', 'endpoints': endpoints}


app.include_router(news.router)
