# Life_Assistant
 My project started as an ambitious idea to solve the daily "what should I wear?" dilemma.
# 🤖 Life Assistant Bot

An intelligent Telegram bot that provides personalized clothing and activity recommendations based on real-time weather data using AI.

## 🌟 Key Features
- **AI-Powered Insights:** Uses LLM (Llama 3 via Groq API) to generate human-like advice based on temperature, humidity, and weather conditions.
- **Daily Automated Forecasts:** Features a background scheduling system that remembers the user's last searched city and sends a fresh update every morning.
- **Smart City Validation:** Integrated with `wttr.in` API with custom logic to handle region-based mismatches (e.g., mapping sub-districts back to major cities).
- **Persistent Memory:** Utilizes an asynchronous SQLite database to store user preferences and search history.

## 🛠 Tech Stack
- **Language:** Python 3.10+
- **Framework:** [Aiogram 3](https://docs.aiogram.dev/) (Asynchronous Telegram Bot API)
- **AI Engine:** [Groq Cloud](https://groq.com/) (Llama-3-70b-versatile)
- **Database:** [Aiosqlite](https://github.com/omnilib/aiosqlite)
- **Task Scheduler:** [APScheduler](https://apscheduler.readthedocs.io/)
- **Weather Source:** [wttr.in](https://wttr.in/)

## 📝 Developer's Note
This project started as an ambitious idea to solve the daily "what should I wear?" dilemma. 

**Personal Growth:** This project was developed with significant mentorship and guidance from AI (Gemini). It served as my "proving ground" for mastering asynchronous programming (`asyncio`), modular project architecture, and multi-API integration. 

Building this bot taught me how to handle real-world edge cases—from URL encoding issues to circular imports. It represents my transition from writing simple scripts to building functional, automated applications.

## 🚀 Getting Started
1. Clone the repository.
2. Create a `config.py` file with your credentials:
   ```python
   BOT_TOKEN = "your_telegram_bot_token"
   GROQ_API_KEY = "your_groq_api_key"
   DB_NAME = "data/life_assistant.db"
