import requests
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
            return self.get_trending(soup)
        else:
            print('Bad request')
            return []

    def get_trending(self, soup):
        try:
            trend_section = soup.find_all('div', class_='SummaryItemWrapper-gdEuvf gVabsw summary-item summary-item--has-margin-spacing summary-item--has-border summary-item--article summary-item--no-icon summary-item--text-align-left summary-item--layout-placement-text-below-desktop-only-thumbnail summary-item--layout-position-image-right summary-item--layout-proportions-33-66 summary-item--side-by-side-align-center summary-item--standard SummaryCollectionRowItem-fjJsDI hfkeds')
            topic_details = []
            if trend_section is None:
                print('Error, could not get trending news')
                return []
            for i in trend_section:
                try:
                    topic = i.find(
                        'h3', class_='SummaryItemHedBase-dZmlME fEkmfC summary-item__hed').text
                    link = i.find(
                        'a', class_='SummaryItemHedLink-cgPsOZ cEGVhT summary-item-tracking__hed-link summary-item__hed-link').get('href')
                    topic_details.append(
                        {"topic": topic, "url": link, "source": "Wired"})
                except Exception:
                    print('Error, could not get trending news')
                    return []
            return topic_details
        except Exception:
            return []
