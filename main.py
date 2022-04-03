from src import *


news = input('Hi there!!\n What website do you want news from?\n 1. Cnet\n 2. Mashable\n 3. Wired\n>>> ')
if news == '1':
    cnet.Cnet().start_crawl()
elif news == '2':
    mashable.Mashable().start_crawl()
elif news == '3':
    wired.Wired().start_crawl()
else: 
    print("Invalid input")