import requests
from bs4 import BeautifulSoup


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
            return self.get_trending(soup)
        else:
            print('Bad request')
            return []

    def get_trending(self, soup):
        try:
            trend_section = soup.find_all('article', class_='meteredContent')
            topic_details = []
            for i in trend_section:
                topic = i.find('h2').text
                link = self.base_url + \
                    i.find('a', {'class': 'au av aw ax ay az ba bb bc bd be bf bg bh bi',
                        'aria-label': 'Post Preview Title'}).get('href')
                topic_details.append({"topic": topic, "url": link, "source": "Medium"})

            return topic_details
        except Exception:
            return []

