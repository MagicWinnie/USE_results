import time
import json
from telegram.client import Telegram

with open("login_data.json", "r", encoding="utf-8") as login_json:
    login_data = json.load(login_json)

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

response = tg.send_message(604005377, "Пришли результаты ЕГЭ!")
response.wait()

time.sleep(2)
tg.stop()
