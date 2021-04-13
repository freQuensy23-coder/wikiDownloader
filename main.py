import requests
from bs4 import BeautifulSoup as BS
from Page import *
import pywikibot
import logging
from tqdm import tqdm

import threading
from ThreadingManager import *

site = pywikibot.Site('ru', 'wikipedia')
parser = "html5lib"


def get_pages_data(pages: list, session=session, site=site):
    """Get information about pages and save them to db
    :param pages list of string - pages names
    :param session SQLAlchemy session object
    :param site pywikibot site object
    :returns True if everything is good
    """
    for page_name in pages:
        try:
            pywiki_page = pywikibot.Page(site, page_name)
            page = Page(title=pywiki_page.title(), text=pywiki_page.text)
            session.add(page)
        except Exception as e:
            logging.critical(e)
            logging.critical(f"Can't add to db {page_name}")
    return True


def get_pages(start_from = "") -> list:
    """Get all pages from page of pages (ex. https://ru.wikipedia.org/w/index.php?title=Служебная:Все_страницы )
    :param start_from return articles from one page, starting from start from
    """
    link = f"https://ru.wikipedia.org/w/index.php?title=Служебная:Все_страницы?from={start_from}"
    r = requests.get(link)
    soup = BS(r.content, parser)
    pages_area = soup.find("div", {"class": "mw-allpages-body"})
    page_names = pages_area.find_all("a")
    for i, page_name in enumerate(page_names):
        page_names[i] = page_name.get_text()
    return page_names


def main():
    global main_link
    pages = get_pages("")
    pages_tasks = tasks_divider(tasks=pages)
    threads = generate_threads(pages_tasks, get_pages_data)
    for t in threads: # start all threads
        t.start()
    for t in tqdm(threads):
        t.join()  # Waiting for process end checking
        # TODO Исправить прогрессбар. Он не должен ждать невыолненные потоки.
    session.commit()


if __name__ == '__main__':
    d = input("Delete everything from DB? (y/N)? ")
    if d.strip().lower() == "y":
        session.execute("DELETE from Pages WHERE 1;")
        session.commit()
    main()
