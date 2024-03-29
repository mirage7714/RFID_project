# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, request, render_template, send_from_directory
import json
from datetime import datetime
import sqlite3
import requests
from bookParser import parseBookData
import pandas as pd

import json

app = Flask(__name__)
app.static_folder = 'static'

main_url = 'https://sheetdb.io/api/v1/24sxv08ychzzl'
book_url = 'https://sheetdb.io/api/v1/24sxv08ychzzl?sheet=book_list'
history_url = 'https://sheetdb.io/api/v1/24sxv08ychzzl?sheet=book_history'

def getStatistics():
    results = {}
    history = {}
    books = []
    book_query = json.loads(requests.get(book_url).text)
    history_query = json.loads(requests.get(history_url).text)
    for his in history_query:
        isbn = his['ISBN']
        if isbn in history.keys():
            history[isbn] += 1
        else:
            history[isbn] = 1
    for book in book_query:
        isbn = book['ISBN']
        if isbn in history.keys():
            books.append({
                'ISBN': isbn,
                'Name': book['Name'],
                'count': history[isbn]
            })
        else:
            books.append({
                'ISBN': isbn,
                'Name': book['Name'],
                'count': 0
            })
    return books

def updateHistory(result):
    index = len(json.loads(requests.get(history_url).text)) + 1
    history_payload = {}
    data = []
    data.append({
            'No': index,
            'ISBN': result[0]['ISBN'],
            'Name': result[0]['Name'],
            'Date': datetime.strftime(datetime.now(), '%Y/%m/%d')
            })
    history_payload['data'] = data
    requests.post(history_url, json = history_payload)
    
@app.route('/')
def index():
    return render_template('index.html')
	
@app.route('/query_book', methods=['POST'])
def Query():
    book = request.form.get('ISBN')
    query = json.loads(requests.get(book_url).text)
    result = []
    for q in query:
        if book == q['ISBN']:
            result.append({
                    'ISBN':q['ISBN'],
                    'Name':q['Name'],
                    'Author': q['Author'],
                    'Publisher': q['Publisher'],
                    'Date': q['Date'],
                    'Status': q['Status']
                    })
    if (len(result) == 0):
        crawlerData = parseBookData(book)
        if (len(crawlerData) > 0 ):
            result.append({
                    "ISBN": book,
                    "Name": crawlerData.split(',')[0],
                    "Author": crawlerData.split(',')[1],
                    "Publisher": crawlerData.split(',')[2],
                    "Date": datetime.strftime(datetime.now(), '%Y/%m/%d'),
                    'Status': 'In'
                    })
            payload = {}
            payload["data"] = result
            print(requests.post(book_url, json = payload))
            updateHistory(result)
    else:
        updateHistory(result)
    return render_template('book.html',book=book,results=result)
	
@app.route('/history')
def history():
    query = json.loads(requests.get(history_url).text)
    result = []
    for row in query:
        result.append({
        'No': row['No'],
        'Name': row['Name'],
        'ISBN': row['ISBN'],
        'Date': row['Date']
        })
    return render_template('history.html',results=result)

@app.route('/statistics')
def statisticsPage():
    result = getStatistics()
    return render_template('statistics.html', results = result)
    
@app.route('/reset')
def reset():
    query = json.loads(requests.get(history_url).text)
    empty = []
    for row in query:
        delete_url = 'https://sheetdb.io/api/v1/24sxv08ychzzl?sheet=book_history/ISBN/{}'.format(row['ISBN'])
        print(delete_url)
        print(requests.delete(delete_url))
    return render_template('reset.html',result = empty)
	
	
if __name__ == "__main__":
    app.run(port=5000, debug = True)