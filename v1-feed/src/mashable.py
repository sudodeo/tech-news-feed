import requests
from . import docx_writer
from bs4 import BeautifulSoup


class Mashable:
    def __init__(self):
        self.sess = requests.Session()
    def start_crawl(self):
        url = 'https://mashable.com/tech'
        self.base_url = 'https://mashable.com'
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
        res = self.sess.get(url, headers=headers)
        if res.ok:
            soup = BeautifulSoup(res.text, 'lxml')
            self.get_trending(soup)
        else:
            print('Bad request')

    def get_trending(self, soup):
        trend_section = soup.find(
            'div', class_='flex flex-row overflow-x-auto space-x-8 overflow-y-hidden')
        topic_list = []
        link_list = []
        if trend_section is None:
            print('Error, could not get trending news')
            return
        trends = trend_section.find_all('div', class_='flex-1')
        if trends is []:
            return
        for i in trends:
            try:
                topic = i.find(
                    'a', class_='block w-full text-lg font-bold leading-6 mt-2').text
                link = self.base_url + i.find('a').get('href')
                topic_list.append(topic)
                link_list.append(link)
            except Exception:
                print('Error, could not get trending news')
                return

        topic_details = list(zip(topic_list, link_list))
        if topic_details is []:
            print('Error, could not get trending news')
            return
        self.output_news_list(topic_details)

    def output_news_list(self, topic_details):
        for index, content in enumerate(topic_details):
            print('\n', index + 1, content[0])
        print('\nSelect a news to view or input 0 to view all')
        choice = input('>>>>> ')
        if choice == '0':
            for i in range(len(topic_details)):
                link = topic_details[i][1]
                res2 = self.sess.get(link)
                if res2.ok:
                    self.get_news(res2)
                else:
                    print('Bad request')
        else:
            for i in range(len(topic_details)):
                if choice == f'{i + 1}':
                    link = topic_details[i][1]
                    res2 = self.sess.get(link)
                    if res2.ok:
                        self.get_news(res2)
                    else:
                        print('Bad request')

    def get_news(self, res):
        soup = BeautifulSoup(res.text, 'lxml')
        try:
            post_title = soup.find(
                'h1', class_='mt-4 header-100 max-w-5xl').text.strip()
            paragraph_chunk = soup.find(
                'article', class_='editor-content mt-8 font-serif').find_all('p')
            paragraphs = [paragraph.text for paragraph in paragraph_chunk]
            link = res.url
            docx_writer.WriteDoc(post_title, paragraphs, link).write_file()
        except Exception:
            print('Error processing docx file')