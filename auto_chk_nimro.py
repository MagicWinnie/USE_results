import time
from datetime import datetime
import random
import json
import requests
from telegram.client import Telegram

import nimro

with open("login_data.json", "r", encoding="utf-8") as login_json:
    login_data = json.load(login_json)

result = 0

_, news = nimro.get_updates('')
flag = False

print('[' + datetime.now().strftime("%H:%M:%S") + ']', "последняя новость на данный момент:")
print(news)

while True:
    curr_hour = datetime.now().hour
    if 18 <= curr_hour < 21:
        delay = 1800
    elif 21 <= curr_hour or curr_hour == 0: 
        delay = 600
    else:
        delay = 3600
    print(f"Жду {delay} секунд")
    time.sleep(delay + random.randint(-30, 30))

    try:
        flag, tmp = nimro.get_updates(news)
        if tmp:
            news = tmp
    except requests.exceptions.Timeout:
        result = -1
        break
    except requests.exceptions.ConnectionError:
        result = -2    
    
    if flag:
        result = 1
        break
    else:
        print('[' + datetime.now().strftime("%H:%M:%S") + ']', 'нет новых новостей')
    # time.sleep(delay + random.randint(-30, 30))

if result == 1:
    print('[' + datetime.now().strftime("%H:%M:%S") + ']', "новая новость!")
    print(news)
elif result == -1:
    print("Превышено время ожидания сервера.")
elif result == -2:
    print("Отсутствует подключение к интернету.")
    exit(0)

# TELEGRAM
tg = Telegram(
    api_id=login_data["api_id"],
    api_hash=login_data["api_hash"],
    phone=login_data["phone"],
    database_encryption_key=login_data["database_encryption_key"],
    tdlib_verbosity=0
)
tg.login()

response = tg.get_chats()
response.wait()

message = "Новая новость!\n" + news if result == 1 else "Превышено время ожидания сервера"
response = tg.send_message(604005377, message)
response.wait()

time.sleep(2)

tg.stop()
