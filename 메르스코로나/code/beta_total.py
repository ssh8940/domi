from bs4 import BeautifulSoup
import requests
import traceback
import pandas as pd
import datetime
import os
import urllib.request

# root = 'kosdaq'

data = pd.DataFrame([])

kospi_list = pd.read_csv('data/kospi_list.csv')
kospi_list = pd.DataFrame(kospi_list, columns=['번호','종목코드','na','기업명'])
kospi_list['na'] = pd.to_numeric(kospi_list['종목코드'])
kospi_list.na = kospi_list.na.map('{:06d}'.format)

kosdaq_list = pd.read_csv('data/kosdaq_list.csv')
kosdaq_list = pd.DataFrame(kosdaq_list, columns=['번호','종목코드','na','기업명'])
kosdaq_list['na'] = pd.to_numeric(kosdaq_list['종목코드'])
kosdaq_list.na = kosdaq_list.na.map('{:06d}'.format)


url2 = "https://finance.naver.com/sise/sise_group_detail.nhn?type=theme&no=346"
html = urllib.request.urlopen(url2) 
o = BeautifulSoup(html, "html.parser") 
l = o.findAll("div", {"class":"name_area"})

for i in range(0,len(l)):
    stock_name = l[i].a.get('href').rsplit('?')[1]
    stock_name = stock_name.split('=')[1]
    stock_kor = l[i].text
    stock_kor = stock_kor.replace("*","")
    # print(stock_kor)
    data = data.append(pd.DataFrame([[i, stock_name, stock_kor]], columns=['no', 'name', 'kor']), ignore_index=True)


data.set_index('no', inplace=True)
data['na'] = pd.to_numeric(data['name'])
data.na = data.na.map('{:06d}'.format)

for n in range(len(data['na'])):
    code = data['na'][n]
    stock_kor = l[n].text
    stock_kor = stock_kor.replace("*","")
    for i in range(len(kosdaq_list['na'])):
        kosdaq_r = kosdaq_list['na'][i]
        try:
            kospi_r = kospi_list['na'][i]
        except KeyError:
            pass
        if code==kospi_r:
            root = 'kospi'
            print(root)
            stock=[]
            stock = pd.read_csv('data/2020-crawling/{root}/{code}.csv'.format(root=root, code=code))
            y = stock['rate']
            kospi=[]
            kospi = pd.read_csv('data/2020-crawling/{root}/KOSPI.csv'.format(root=root))
            x = kospi['kospi']

            z=[]
            z = pd.concat([y, x], axis=1)
            cov = z.cov()['rate'][1]

            var = x.var()

            beta = cov/var
            print(beta)
            stock = stock.append(pd.DataFrame([[beta]],columns=['BETA']))
            # print(stock)

            # stock['BETA'] = beta
            # print(stock)

            path_dir = 'data/2020-stock'
            #회사명
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            path = os.path.join(path_dir, '{kor}.csv'.format(kor=stock_kor))
            stock.to_csv(path, encoding = 'utf-8-sig',index=False)
            #코드명
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            path = os.path.join(path_dir, '{code}.csv'.format(code=code))
            stock.to_csv(path, encoding = 'utf-8-sig',index=False)
        elif code==kosdaq_r:
            root = 'kosdaq'
            print(root)
            stock=[]
            stock = pd.read_csv('data/2020-crawling/{root}/{code}.csv'.format(root=root, code=code))
            y = stock['rate']
            kosdaq=[]
            kosdaq = pd.read_csv('data/2020-crawling/{root}/KOSDAQ.csv'.format(root=root))
            x = kosdaq['kosdaq']

            z=[]
            z = pd.concat([y, x], axis=1)
            cov = z.cov()['rate'][1]

            var = x.var()

            beta = cov/var
            print(beta)
            stock = stock.append(pd.DataFrame([[beta]],columns=['BETA']))
            # print(stock)

            # stock['BETA'] = beta
            # print(stock)

            path_dir = 'data/2020-stock'
            #회사명
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            path = os.path.join(path_dir, '{kor}.csv'.format(kor=stock_kor))
            stock.to_csv(path, encoding = 'utf-8-sig',index=False)
            #코드명
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            path = os.path.join(path_dir, '{code}.csv'.format(code=code))
            stock.to_csv(path, encoding = 'utf-8-sig',index=False)
