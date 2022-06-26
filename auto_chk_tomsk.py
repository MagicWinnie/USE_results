import time
from datetime import datetime
import random
import json
import pandas as pd
import requests
from telegram.client import Telegram

import coko_tomsk

with open("login_data.json", "r", encoding="utf-8") as login_json:
    login_data = json.load(login_json)

result = 0

prev_df_tomsk = pd.DataFrame()
_, prev_df_tomsk, _ = coko_tomsk.get_updates(prev_df_tomsk)

print('[' + datetime.now().strftime("%H:%M:%S") + ']', "результаты на данный момент:")
print(prev_df_tomsk)

while True:
    curr_hour = datetime.now().hour
    if 18 <= curr_hour < 21:
        delay = 1800
    elif 21 <= curr_hour or curr_hour == 0: 
        delay = 900
    else:
        delay = 3600
    print(f"Жду {delay} секунд")
    time.sleep(delay + random.randint(-30, 30))

    try:
        flag_tomsk, _, diff_tomsk = coko_tomsk.get_updates(prev_df_tomsk)
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.ConnectionError:
        pass

    if flag_tomsk:
        result = 1
        break
    else:
        print('[' + datetime.now().strftime("%H:%M:%S") + ']', 'нет результатов')
    # time.sleep(delay + random.randint(-30, 30))

if result == 1:
    print('[' + datetime.now().strftime("%H:%M:%S") + ']', "возможно пришли результаты!")
    print("Изменения ЦОКО Томск (первые 5 строчек):")
    print(diff_tomsk.head(5))
elif result == -1:
    print("Превышено время ожидания сервера. Возможно пришли результаты.")
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

if result == 1:
    message = "Пришли результаты ЕГЭ!\n"
    message += diff_tomsk.to_string()
else:
    message = "Превышено время ожидания сервера"
response = tg.call_method(
    "sendMessage",
    params={
        "chat_id": login_data["chat_id"],
        "input_message_content": {
            "@type": "inputMessageText",
            "text": {"@type": "formattedText", "text": message},
        },
    },
)
response.wait()

time.sleep(2)

tg.stop()
