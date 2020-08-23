from bs4 import BeautifulSoup
import requests
import traceback
import pandas as pd
import datetime
import os
import urllib.request

url = "https://finance.naver.com/sise/sise_group_detail.nhn?type=theme&no=436"
html = urllib.request.urlopen(url) 
o = BeautifulSoup(html, "html.parser") 
l = o.findAll("div", {"class":"name_area"})

data = pd.DataFrame([])
for i in range(0,len(l)):
    stock_name = l[i].a.get('href').rsplit('?')[1]
    stock_name = stock_name.split('=')[1]
    stock_kor = l[i].text
    stock_kor = stock_kor.replace("*","")
    # print(stock_kor)
    data = data.append(pd.DataFrame([[i, stock_name, stock_kor]], columns=['no', 'name', 'kor']), ignore_index=True)

data.set_index('no', inplace=True)
data['na'] = pd.to_numeric(data['name'])
# print(data)
data.na = data.na.map('{:06d}'.format)
# print(data)
for n in range(len(data)):
    code = data['na'][n]
    df = pd.read_csv('data/2020-crawling/{code}.csv'.format(code=code))
    df = pd.DataFrame(df, columns=['날짜','종가','전일비','시가','고가','저가','거래량','rate'])
    df['rate'] = df['종가'].diff()/df['종가']*100
    path_dir = 'data/2020-crawling'
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    path = os.path.join(path_dir, '{code}.csv'.format(code=code))

    df.to_csv(path, encoding = 'utf-8-sig',index=False)
    print(df)

