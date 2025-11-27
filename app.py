import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Берём токен из Render
PDF_LINK = os.environ.get("PDF_LINK")  # Ссылка на PDF или закрытый TG-канал

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('status') == 'succeeded':
        chat_id = data.get('client_chat_id')
        send_message(chat_id, f"Спасибо за оплату! Вот ваш доступ: {PDF_LINK}")
    return "ok", 200

if __name__ == "__main__":
    app.run(port=5000)
