import requests
from bs4 import BeautifulSoup as BS
from Page import *

parser = "html5lib"


def get_page_data(link):
    r = requests.get(link)
    soup = BS(r.content,  parser)
    pages_area = soup.find("div", {"class":"mw-allpages-body"})
    links = pages_area.find_all("a")
    for link in links:
        print(link)
        page = Page(link = link.get("href"), title = link.get_text())
        print(page)


def main():
    pass


if __name__ == '__main__':
    main_link = "https://ru.wikipedia.org/w/index.php?title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%92%D1%81%D0%B5_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%8B&from=.%E0%B9%84%E0%B8%97%E0%B8%A2"
    get_page_data(main_link)
