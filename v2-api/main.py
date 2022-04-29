from fastapi import FastAPI
from .routers import news


app = FastAPI()


@app.get('/')
def home():
    endpoints = {"combined news": "/news", "cnet": "/news/cnet", "mashable": "/news/mashable",
                 "medium": "/news/medium", "the next web": "/news/tnw", "wired": "news/wired"}
    return {'Tech News': 'Get top trending news via this API', 'endpoints': endpoints}


app.include_router(news.router)
