import requests
from . import docx_writer
from bs4 import BeautifulSoup


class Wired:
    def __init__(self):
        self.sess = requests.Session()

    def start_crawl(self):
        url = 'https://www.wired.com/'
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
        res = self.sess.get(url, headers=headers)
        if res.ok:
            soup = BeautifulSoup(res.text, 'lxml')
            self.get_trending(soup)
        else:
            print('Bad request')

    def get_trending(self, soup):
        trend_section = soup.find_all('div', class_='SummaryItemWrapper-gdEuvf gVabsw summary-item summary-item--has-margin-spacing summary-item--has-border summary-item--article summary-item--no-icon summary-item--text-align-left summary-item--layout-placement-text-below-desktop-only-thumbnail summary-item--layout-position-image-right summary-item--layout-proportions-33-66 summary-item--side-by-side-align-center summary-item--standard SummaryCollectionRowItem-fjJsDI hfkeds')
        topic_list = []
        link_list = []
        if trend_section is None:
            print('Error, could not get trending news')
            return
        for i in trend_section:
            try:
                topic = i.find(
                    'h3', class_='SummaryItemHedBase-dZmlME fEkmfC summary-item__hed').text
                link = i.find(
                    'a', class_='SummaryItemHedLink-cgPsOZ cEGVhT summary-item-tracking__hed-link summary-item__hed-link').get('href')
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
                'h1', class_='BaseWrap-sc-TURhJ BaseText-fFzBQt ContentHeaderHed-kpvpFG eTiIvU bVPdwx kjQZOs').text.strip()
            paragraph_chunk = soup.find(
                'div', {'data-testid': 'ArticlePageChunks'}).find_all('p')
            paragraphs = [paragraph.text for paragraph in paragraph_chunk]
            link = res.url
            docx_writer.WriteDoc(post_title, paragraphs, link).write_file()
        except Exception:
            print('Error processing docx file')