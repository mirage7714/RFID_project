# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:28:21 2019

@author: mirag
"""
import requests
from bs4 import BeautifulSoup as soup

def parseBookData(isbn):
    url = 'https://search.books.com.tw/search/query/key/{}/cat/all'.format(isbn)
    content = soup(requests.get(url).text, 'lxml')
    results = content.find_all('li',{'class':'item'})
    name = ''
    author = ''
    if (len(results) > 0 ):
        name = results[0].find('a')['title']
        author = results[0].find('a',{'rel':'go_author'})['title']
        publisher = results[0].find('a',{'rel':'mid_publish'})['title']
    return ('{},{},{}'.format(name, author, publisher))