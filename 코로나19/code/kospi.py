from bs4 import BeautifulSoup
import requests
import traceback
import pandas as pd
import datetime
import os

code = 'KOSPI'  # NAVER
root = 'kospi'
url = 'https://finance.naver.com/sise/sise_index_day.nhn?code={code}'.format(code=code)
res = requests.get(url)
print(url)
res.encoding = 'utf-8'
soap = BeautifulSoup(res.text, 'lxml')

el_table_navi = soap.find("table", class_="Nnavi")
el_td_last = el_table_navi.find("td", class_="pgRR")
pg_last = el_td_last.a.get('href').rsplit('&')[1]
pg_last = pg_last.split('=')[1]
pg_last = int(pg_last)
# print(pg_last)

def parse_page(code, page):
    try:
        url = 'https://finance.naver.com/sise/sise_index_day.nhn?code={code}&page={page}'.format(code=code, page=page)
        res = requests.get(url)
        _soap = BeautifulSoup(res.text, 'lxml')
        _df = pd.read_html(str(_soap.find("table")), header=0)[0]
        _df = _df.dropna()
        return _df
    except Exception as e:
        traceback.print_exc()
    return None

str_datefrom = datetime.datetime.strftime(datetime.datetime(year=2019, month=12, day=27), '%Y.%m.%d')
print(str_datefrom)

str_dateto = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')
print(str_dateto)

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

print(df)
df=df.sort_values(by=['날짜'], axis=0)
df['kospi'] = df['전일비']/df['체결가']*100
print(df, df.dtypes, df.columns)
path_dir = 'data/2020-crawling/{root}'.format(root=root)
if not os.path.exists(path_dir):
    os.makedirs(path_dir)
path = os.path.join(path_dir, '{code}.csv'.format(code=code))

df.to_csv(path, encoding = 'utf-8-sig',index=False)

path_dir = 'data/2020-crawling/{root}'.format(root=root)
if not os.path.exists(path_dir):
    os.makedirs(path_dir)
path = os.path.join(path_dir, '{code}.csv'.format(code=code))

df.to_csv(path, encoding = 'utf-8-sig',index=False)