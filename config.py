import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_NAME = "data/life_assistant.db"


if not BOT_TOKEN:
    exit("Ошибка: Токен бота не найден. Проверь .env файл!")