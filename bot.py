import telebot
import requests
from io import BytesIO
import concurrent.futures
import requests
from my_site import keep_alive

TOKEN = "7354603386:AAGoT1hrPwjoAd_s_XSgvFvQx8CjeWJdb1o"
CHAT_ID = 123456789  # ID твоего чата или юзера

import re

list_ = []

pattern = re.compile(r'^(?:vless|vmess|ss)://.*(?:🇷🇺|\bss-RU\b)', re.IGNORECASE)

bot = telebot.TeleBot(TOKEN)

URLS = [
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt" #6
]

def fetch_file(url: str) -> tuple[str, BytesIO] | None:
    """Скачивает файл и возвращает (имя, содержимое)"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # Определяем корректное имя файла с .txt
        filename = url.split("/")[-1]
        if not filename:
            filename = "file.txt"
        if not filename.endswith(".txt"):
            filename += ".txt"
        
        content = BytesIO(response.content)
        content.name = filename  # нужно для telebot
        return filename, content
    except Exception as e:
        print(f"⚠️ Ошибка при скачивании {url}: {e}")
        return None

def main(chat_id, id_):
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(fetch_file, URLS))


    bot.delete_message(chat_id=chat_id, message_id=id_)
    for result in results:
        if result:
            filename, content = result
            try:
                # bot.send_document(chat_id, content, caption=f"📄 {filename}").id
                print(f"✅ Отправлен {filename}")
            except Exception as e:
                print(f"⚠️ Ошибка при отправке {filename}: {e}")

            if filename == "V2RAY_RAW.txt":
                content.seek(0)
                text = content.read().decode('utf-8')

                for line in text.splitlines():
                    if a := pattern.search(line):
                        list_.append(f"🇷🇺 `{a.group(0).replace(' ss-RU', '')}`")

    mes = '\n\n'.join(list_)
    bot.send_message(chat_id=chat_id, text=mes , parse_mode="Markdown")

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    id_ = bot.reply_to(message, """Начинаю сбор файлов...📥""").id
    main(chat_id=message.chat.id, id_=id_)

keep_alive()
bot.infinity_polling(skip_pending=True)
