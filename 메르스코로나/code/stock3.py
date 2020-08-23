from bs4 import BeautifulSoup
import requests
import traceback
import pandas as pd
import datetime
import os
import urllib.request

str_datefrom = datetime.datetime.strftime(datetime.datetime(year=2019, month=12, day=27), '%Y.%m.%d')
print(str_datefrom)

str_dateto = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')
print(str_dateto)

def parse_page(code, page):
        try:
            url = 'http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'.format(code=code, page=page)
            res = requests.get(url)
            _soap = BeautifulSoup(res.text, 'lxml')
            _df = pd.read_html(str(_soap.find("table")), header=0)[0]
            _df = _df.dropna()
            return _df
        except Exception as e:
            traceback.print_exc()
        return None


url2 = "https://finance.naver.com/sise/sise_group_detail.nhn?type=theme&no=346"
html = urllib.request.urlopen(url2) 
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
data.na = data.na.map('{:06d}'.format)
for n in range(len(data)):
    code = data['na'][n]
    stock_kor = l[n].text
    stock_kor = stock_kor.replace("*","")
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    print(url)
    res = requests.get(url)
    res.encoding = 'utf-8'
    soap = BeautifulSoup(res.text, 'lxml')
    el_table_navi = soap.find("table", class_="Nnavi")
    el_td_last = el_table_navi.find("td", class_="pgRR")
    pg_last = el_td_last.a.get('href').rsplit('&')[1]
    pg_last = pg_last.split('=')[1]
    pg_last = int(pg_last)
    print(pg_last)
    df = None
    for page in range(1, pg_last+1):
        _df = parse_page(code, page)
        _df_filtered = _df[_df['날짜'] > str_datefrom]
        if df is None:
            df = _df_filtered
        else:
            df = pd.concat([df, _df_filtered])
        if len(_df) > len(_df_filtered):
            break

    # print(df)
    df=df.sort_values(by=['날짜'], axis=0)

    path_dir = 'data/2020-crawling'
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    path = os.path.join(path_dir, '{kor}.csv'.format(kor=stock_kor))
    df.to_csv(path, encoding = 'utf-8-sig',index=False)

    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    path = os.path.join(path_dir, '{code}.csv'.format(code=code))
    df.to_csv(path, encoding = 'utf-8-sig',index=False)