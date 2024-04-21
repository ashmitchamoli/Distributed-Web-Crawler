import sys
import zipimport

importer = zipimport.zipimporter('library.mod')
bs4 = importer.load_module('bs4')
BeautifulSoup = bs4.BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse


def scrape_urls(url):
    try:
        with urlopen(url) as response:
            soup = BeautifulSoup(response.read(), 'html.parser')
            links = soup.find_all('a')
            urls = []
            for link in links:
                href = link.get('href')
                if href:
                    parsed_href = urlparse(href)
                    if parsed_href.scheme in ('http', 'https'):
                        urls.append(href)
            return list(set(urls))
    except:
        return []


for line in sys.stdin:
    line = line.strip()
    page, state = line.split()
    if page[-1] == '/':
        page = page[:-1]
    if state == '0':
        state = int(state)
    if state == 0:  # not crawled
        print(page, state)
        urls = scrape_urls(page)
        if len(urls) > 0:
            print(page, *urls)
            for url in urls:
                print(url, 0)
        else:
            print(page, -1)
    else:  # already crawled
        print(page, 1)
