import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_updates(to_cmp: str):
    request = requests.get("https://www.nimro.ru/news", timeout=6)
    request.encoding = "utf-8"
    page = request.text

    soup = BeautifulSoup(page, features="lxml")
    news = soup.find('div', class_='news-list').find('div', class_='news-list__title').text.strip()

    if news != to_cmp:
        return (True, news)
    else:
        return (False, '')

if __name__ == "__main__":
    prev_file = "prev_news.txt"
    if prev_file not in os.listdir('.'):
        prev = ''
    else:
        with open(prev_file, 'r', encoding='utf-8') as infile:
            prev = infile.readline().strip()

    flag, news = get_updates(prev)

    if not flag:
        print("Новых новостей нет")
    else:
        print("Новая новость:")
        print(news)
        with open(prev_file, 'w', encoding='utf-8') as outfile:
            outfile.write(news)
