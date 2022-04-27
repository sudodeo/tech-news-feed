import requests

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
            return self.get_trending(soup)
        else:
            print('Bad request')
            return []

    def get_trending(self, soup):
        try:
            trend_section = soup.find(
                'div', class_='flex flex-row overflow-x-auto space-x-8 overflow-y-hidden')
            topic_details = []
            if trend_section is None:
                print('Error, could not get trending news')
                return []
            trends = trend_section.find_all('div', class_='flex-1')
            if trends is []:
                return []
            for i in trends:
                try:
                    topic = i.find(
                        'a', class_='block w-full text-lg font-bold leading-6 mt-2').text
                    link = self.base_url + i.find('a').get('href')
                    topic_details.append({"topic": topic, "url": link, "source": "Mashable"})
                except Exception:
                    print('Error, could not get trending news')
                    return []

            return topic_details
        except Exception:
            return []