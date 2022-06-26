import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_updates(to_cmp:pd.DataFrame):
    request = requests.get("http://nscm.ru/egeresult/resultform.php", timeout=6)
    request.encoding = "utf-8"
    page = request.text

    soup = BeautifulSoup(page, features="lxml")
    table = soup.find('table', id='res_data_table')

    df = pd.read_html(table.prettify())[0]
    df.columns = ["Дата", "Предмет"]

    diff = pd.concat([df, to_cmp]).drop_duplicates(keep=False)
    if diff.empty:
        return (False, pd.DataFrame(), pd.DataFrame())
    else:
        return (True, df, diff)

if __name__ == "__main__":
    prev_file = "prev_file.csv"
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
