import os
import telebot
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
PDF_LINK = os.environ['PDF_LINK']

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- Команды бота ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я СММ-маркетолог и покажу путь к продажам! Напиши /ценность")

@bot.message_handler(commands=['ценность'])
def value(message):
    bot.send_message(message.chat.id, "Ты получаешь мини-стратегию, шаблоны, чек-листы и промпты для анализа аудитории.")
    bot.send_message(message.chat.id, "Напиши /пример чтобы увидеть мини-пример стратегии.")

@bot.message_handler(commands=['пример'])
def example(message):
    bot.send_message(message.chat.id, "Пример мини-воронки: анализ ЦА → контент-план → пост с призывом. Для полного доступа напиши /оплата")

@bot.message_handler(commands=['оплата'])
def payment(message):
    bot.send_message(message.chat.id, f"Оплати курс и получи доступ: {PDF_LINK}")

# --- Webhook ---
@app.route(f"/{TELEGRAM_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# Настройка webhook
bot.remove_webhook()
bot.set_webhook(url=f"https://minisalesbot.onrender.com/{TELEGRAM_TOKEN}")

if __name__ == "__main__":
    # Render запускает через gunicorn, поэтому здесь только Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
