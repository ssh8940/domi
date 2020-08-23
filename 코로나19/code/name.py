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

print(data)