import requests
from docx_writer import WriteDoc
from bs4 import BeautifulSoup


############## NEED TO WRITE HTML TO DOCX BECAUSE OF PICTURES #####################
class Medium:
    def __init__(self) -> None:
        pass
    def start_crawl(self):
        url = 'https://medium.com/tag/programming'
        self.base_url = 'https://medium.com'
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
        res = requests.get(url, headers=headers)
        if res.ok:
            soup = BeautifulSoup(res.text, 'lxml')
            self.get_trending(soup)
        else:
            print('Bad request')
    def get_trending(self, soup):
        trend_section = soup.find_all('article', class_='meteredContent')
        topic_list = []
        link_list = []
        for i in trend_section:
            topic = i.find(
                'h2', class_='bo fw kl km kn ko ga kp kq kr ks ge kt ku kv kw gi kx ky kz la gm lb lc ld le gq gr gs gt gv gw fu').text
            link = self.base_url + i.find('a', {'class':'au av aw ax ay az ba bb bc bd be bf bg bh bi', 'aria-label':'Post Preview Title'}).get('href')
            topic_list.append(topic)
            link_list.append(link)

        topic_details = list(zip(topic_list, link_list))
        self.output_news_list(topic_details)
    def output_news_list(self, topic_details):
        for index, content in enumerate(topic_details):
            print(index + 1, content[0])
        print('Select a news to view or input 0 to view all')
        choice = input('>>>>> ')
        if choice == '0':
            for i in range(len(topic_details)):
                link = topic_details[i][1]
                res2 = requests.get(link)
                if res2.ok:
                    self.get_news(res2)
                else:
                    print('Bad request')
        else:
            for i in range(len(topic_details)):
                if choice == f'{i + 1}':
                    link = topic_details[i][1]
                    res2 = requests.get(link)
                    if res2.ok:
                        self.get_news(res2)
                    else:
                        print('Bad request')
    def get_news(self, res):
        soup = BeautifulSoup(res.text, 'lxml')
        post_title = soup.find(
            'h1', id='5f8f').text.strip()
        paragraph_chunk = soup.find(
            'div', {'data-testid': 'ArticlePageChunks'}).find_all('p')
        paragraphs = [paragraph.text for paragraph in paragraph_chunk]
        link = res.url
        WriteDoc(post_title, paragraphs, link).write_file()

ed = Medium()
ed.start_crawl()