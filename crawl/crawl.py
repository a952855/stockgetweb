#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
prototype.py
For building the stock get features.
"""

import urllib.request as req
import bs4
import json
import time
import random
import requests
import pandas as pd

HEADERS = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
           "like Gecko) Chrome/75.0.3770.100 Safari/537.36")


def crawlSelectType():
    url = 'https://www.twse.com.tw/zh/page/trading/exchange/BFT41U.html'
    request = req.Request(url, headers={'User-Agent': HEADERS})
    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')
    root = bs4.BeautifulSoup(data, 'html.parser')
    select = root.find("select", class_='board')
    indexes = [str(x+1).zfill(2) for x in range(31)]
    selectTypes = dict()
    for t in select:
        if t.string != '\n' and t['value'] in indexes:
            selectTypes[t['value']] = t.string
    return selectTypes


def crawlStockBasis(_type='', date=''):
    time.sleep(random.randint(0, 10))
    url = ("https://www.twse.com.tw/exchangeReport/BWIBBU_d?"
           f"response=json&date=&selectType={_type}&_={date}")
    request = requests.get(url, headers={'User-Agent': HEADERS})
    data = bs4.BeautifulSoup(request.content, 'html.parser')
    jsonData = json.loads(data.text)
    if jsonData['stat'] == 'OK':
        columns = ['StockNo', 'StockName', 'Yield', 'Year', 'PE', 'PB', 'YQ']
        dfStock = pd.DataFrame(jsonData['data'], columns=columns)
        dfStock['type'] = _type
        return dfStock
    return pd.DataFrame()


def crawlRoeRoa(_id):
    time.sleep(random.randint(0, 10))
    url = ("https://histock.tw/stock/financial.aspx?"
           f"no={_id}&t=3&st=2&q=3")
    try:
        request = requests.get(url, headers={'User-Agent': HEADERS})
        root = bs4.BeautifulSoup(request.text, 'html.parser')
        table = root.find('table', class_="tb-stock tbBasic")
        data = table.find_all('tr')
        # example: \n201832.11%17.34%\n
        strData = data[1].text
        strData = strData.replace('\n', '')[4:]
        roe = strData.split('%')[0]
        roa = strData.split('%')[1]
        return roe, roa
    except:
        return '-', '-'

def crawlEps(_id):
    time.sleep(random.randint(0, 10))
    url = (f"https://histock.tw/stock/{_id}/"
           "%E6%AF%8F%E8%82%A1%E7%9B%88%E9%A4%98")
    try:
        request = requests.get(url, headers={'User-Agent': HEADERS})
        root = bs4.BeautifulSoup(request.text, 'html.parser')
        table = root.find('table', class_="tb-stock text-center tbBasic")
        data = table.find_all('tr')[5].find_all('td')
        for i in range(len(data), -1, -1):
            if data[i].text != '-':
                return data[i].text
    except:
        return '-'


def collectStockData():
    types = crawlSelectType()
    df = pd.DataFrame()
    for t in types:
        df = pd.concat([df, crawlStockBasis(t)], axis=0)

    df.sort_values('StockNo', inplace=True)
    df['type'] = df['StockNo'].apply(lambda x: list(df[df.StockNo == x]['type']))
    df.drop_duplicates(subset='StockNo', inplace=True)
    print('Crawling ROE, ROA ...')
    df[['ROE', 'ROA']] = df['StockNo'].apply(lambda x:
                                             pd.Series(crawlRoeRoa(x)))
    print('Crawing EPS ...')
    df['EPS'] = df['StockNo'].apply(lambda x: crawlEps(x))
    df.to_csv('test.csv', index=False)
    df.set_index('StockNo', inplace=True)
    stocks = df.to_dict('index')
    stocks = {k: json.dumps(v) for k, v in stocks.items()}
    return stocks


if __name__ == '__main__':
    print(collectStockData())
    #df = crawlStockBasis('01')
    #print(df)
    #print(crawlRoeRoa('2025'))
    #print(crawlEps('2025'))

