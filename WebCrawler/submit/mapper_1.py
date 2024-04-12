#!/usr/bin/env python3
# -*-coding:utf-8 -*

import sys
import zipimport

# print("Hello", 0)

importer = zipimport.zipimporter(
    'library.mod'
)
reqImporter = zipimport.zipimporter(
	'requests.mod'
)
bs4 = importer.load_module('bs4')
# reqs = reqImporter.load_module('requests')
# from bs4 import BeautifulSoup
BeautifulSoup = bs4.BeautifulSoup
import http.client

# print("Hello", 1)

def scrape_urls(url):
    try:
        conn = http.client.HTTPSConnection(url)
        conn.request("GET", "/")
        response = conn.getresponse()
        soup = BeautifulSoup(response.read(), 'html.parser')
        conn.close()
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
    if state == '0':
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
