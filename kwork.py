import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse


class KWork:
    host = 'https://kwork.ru'
    url = 'https://kwork.ru/projects?c=11'
    last_key = ""
    last_key_file = "last_key.txt"

    def __init__(self, last_key_file):
        self.last_key_file = last_key_file

        if os.path.exists(last_key_file):
            self.last_key = open(last_key_file, 'r').read()
        else:
            f = open(last_key_file, 'w')
            self.last_key = self.get_last_key()
            f.write(self.last_key)
            f.close()

    def new_projects(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        new = []
        items = html.select('.wants-content > .project-list > .want-card > .card__content > .mb15 > .wants-card__header > .wants-card__header-title > a')

        for item in items:
            key = self.parse_href(item['href'])
            if self.last_key < key:
                new.append(item['href'])

        return new

    def project_info(self, link):
        r = requests.get(link)
        html = BS(r.content, 'html.parser')

        # form data
        info = {
            "id": self.parse_href(link),
            "title": html.select('.project-card > .card__content > .mb15 > .wants-card__header > .wants-card__header-title')[0].text,
            "description": html.select('.project-card > .card__content > .mb15 > .mt10 > .wish_name > div')[0].text,
            "price": html.select('.mb15 > .wants-card__header > .wants-card__header-right-block > .wants-card__header-controls > .wants-card__header-price')[0].text,
            "customer": html.select('.project-card > .card__content > .want-payer-statistic > .dib > div > .dib > a')[0].text,
            "link": link
        }

        return info

    @staticmethod
    def download_image(url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename

    def get_last_key(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        items = html.select('.wants-content > .project-list > .want-card > .card__content > .mb15 > wants-card__header > wants-card__header-title > a')
        return self.parse_href(items[0]['href'])

    @staticmethod
    def parse_href(href):
        result = href.split('/')
        return result[-1]

    def update_last_key(self, new_key):
        self.last_key = new_key

        with open(self.last_key_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()

        return new_key
