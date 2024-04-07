import sys
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

import re

def scrape_urls(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        urls = []
        for link in links:
            href = link.get('href')
            if href and (href.startswith('http://')
                         or href.startswith('https://')):
                urls.append(href)
        return list(set(urls))
    except:
        return []

for line in sys.stdin:
    line = line.strip()
    page, state = line.split()
    if page[-1] == '/':
        page = page[:-1]
    state = int(state)
    if state == 0:  #not crawled
        print(page, state)
        urls = scrape_urls(page)
        if len(urls) == 0:
            print(page, -1)
        else:
            print(page, *urls)
            for url in urls:
                print(url, 0)
        # print("Hello", 1)
    else:
        print(page, 1)
