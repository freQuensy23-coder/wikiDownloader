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

# DATABASE
timeout = 2147482

logging.basicConfig(level=logging.INFO)


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
    link = f"https://ru.wikipedia.org/wiki/Служебная:Все_страницы?from={start_from}"
    r = requests.get(link)
    soup = BS(r.content, parser)
    pages_area = soup.find("div", {"class": "mw-allpages-body"})
    page_names = pages_area.find_all("a")
    for i, page_name in enumerate(page_names):
        page_names[i] = page_name.get_text()
    return page_names


def main():
    global main_link
    articles = get_pages(start_from="!")
    pages_tasks = tasks_divider(tasks=articles)
    threads = generate_threads(pages_tasks, get_pages_data)
    for t in threads: # start all threads
        t.start()
    for t in threads:
        t.join()  # Waiting for process end checking
        # TODO Исправить прогрессбар. Он не должен ждать невыолненные потоки.
    for i in tqdm(range(3)):
        last_article = articles[-1]
        articles = get_pages(start_from=last_article)[1:]
        pages_tasks = tasks_divider(tasks=articles)
        threads = generate_threads(pages_tasks, get_pages_data)
        for t in threads:  # start all threads
            t.start()
        for t in threads:
            t.join()  # Waiting for process end checking
            # TODO Исправить прогрессбар. Он не должен ждать невыолненные потоки.
            # TODO Убрать повторние кода
        session.commit()
        logging.info(f"Last article: {last_article}")


if __name__ == '__main__':
    patch_http_connection_pool(maxsize=50)
    patch_https_connection_pool(maxsize=50)
    d = input("Delete everything from DB? (y/N)? ")
    if d.strip().lower() == "y":
        session.execute("DELETE from Pages WHERE 1;")
    session.execute(f"SET SESSION wait_timeout := {timeout};")
    session.commit()
    main()
