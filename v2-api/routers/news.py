from fastapi import APIRouter
from ..src import cnet, mashable, medium, tnw, wired


router = APIRouter(prefix='/news')


@router.get('/')
def get_all_news():
    cnet_ = cnet.Cnet().start_crawl()
    mashable_ = mashable.Mashable().start_crawl()
    medium_ = medium.Medium().start_crawl()
    tnw_ = tnw.Tnw().start_crawl()
    wired_ = wired.Wired().start_crawl()
    site_collection = [cnet_, mashable_, medium_, tnw_, wired_]
    return [news for site in site_collection for news in site]


@router.get('/cnet')
def get_cnet_news():
    news = cnet.Cnet().start_crawl()
    return news


@router.get('/mashable')
def get_mashable_news():
    news = mashable.Mashable().start_crawl()
    return news


@router.get('/medium')
def get_medium_news():
    news = medium.Medium().start_crawl()
    return news


@router.get('/tnw')
def get_tnw_news():
    news = tnw.Tnw().start_crawl()
    return news


@router.get('/wired')
def get_wired_news():
    news = wired.Wired().start_crawl()
    return news
