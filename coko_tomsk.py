import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_updates(to_cmp:pd.DataFrame):
    request = requests.get("http://coko.tomsk.ru/exam2022/default.aspx", timeout=6)
    request.encoding = "utf-8"
    page = request.text

    soup = BeautifulSoup(page, features="lxml")
    table = soup.find('table', id='ctl00_ContentPlaceHolder1_ExamSummary')

    df = pd.read_html(table.prettify(), header=0)[0]
    df = df[['Экзамен', 'Результатов']]
    df = df[df['Экзамен'].str.contains("-9") == False]

    diff = pd.concat([df, to_cmp]).drop_duplicates(keep=False)
    if diff.empty:
        return (False, pd.DataFrame(), pd.DataFrame())
    else:
        return (True, df, diff)

if __name__ == "__main__":
    prev_file = "prev_file_coko_tomsk.csv"
    if prev_file not in os.listdir('.'):
        df_old = pd.DataFrame()
    else:
        df_old = pd.read_csv(prev_file, encoding="utf-8")

    flag, df, diff = get_updates(df_old)

    if not flag:
        print("Новых результатов нет")
    else:
        print("Новые результаты (первые 5):")
        print(diff.head(5))
        df.to_csv(prev_file, encoding="utf-8", index=False)
