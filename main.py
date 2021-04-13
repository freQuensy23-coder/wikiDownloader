import requests
from bs4 import BeautifulSoup as BS
from Page import *
import pywikibot
import logging
from tqdm import tqdm

site = pywikibot.Site('ru', 'wikipedia')

parser = "html5lib"


def get_page_data(link):
    r = requests.get(link)
    soup = BS(r.content,  parser)
    pages_area = soup.find("div", {"class":"mw-allpages-body"})
    links = pages_area.find_all("a")
    for tag_a in tqdm(links):
        try:
            page_name = tag_a.get_text()
            pywiki_page = pywikibot.Page(site, page_name)
            page = Page(title = pywiki_page.title(), text = pywiki_page.text)
            session.add(page)
        except:
            logging.critical("Can't add to db", tag_a)
    session.commit()


def main():
    pass


if __name__ == '__main__':
    main_link = "https://ru.wikipedia.org/w/index.php?title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%92%D1%81%D0%B5_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%8B&from=.%E0%B9%84%E0%B8%97%E0%B8%A2"
    get_page_data(main_link)
