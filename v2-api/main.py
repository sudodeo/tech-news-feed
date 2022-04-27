from fastapi import FastAPI
from .routers import news


app = FastAPI()


@app.get('/')
def home():
    return {'Tech News': 'Get top trending news via this API'}

app.include_router(news.router)
