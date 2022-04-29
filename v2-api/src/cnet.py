import re
import requests
from bs4 import BeautifulSoup


class Cnet:
    def start_crawl(self):
        url = 'https://www.cnet.com/tech/'
        self.base_url = 'https://cnet.com'
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
            trend_section = soup.find('div', class_='c-premiumCards_canvas')
            topic_details = []
            if trend_section is None:
                print('Error, could not get trending news')
                return []
            trends = trend_section.find_all(
                'div', class_='c-premiumCards_wrapper')
            if trends is []:
                return []
            for i in trends[:10]:
                try:
                    topic = i.find('a', class_='o-linkOverlay').text
                    link = self.base_url + \
                        i.find('a', class_='o-linkOverlay').get('href')
                    topic_details.append(
                        {"topic": topic, "url": link, "source": "Cnet"})
                except Exception as e:
                    print(e)
                    print('Error2, could not get trending news')
                    return []

            return topic_details
        except Exception:
            return []
