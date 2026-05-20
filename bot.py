import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN
from utils.weather import get_weather
from utils.ai import get_ai_recommendation
from utils.db import init_db, set_user_city, get_all_users

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def send_daily_forecast():
    users = await get_all_users()
    for user_id, city in users:
        try:
            w_data = await get_weather(city)
            if w_data:
                advice = await get_ai_recommendation(w_data['temp'], w_data['desc'], w_data['humidity'])
                text = (
                    f"☀️ <b>Доброе утро!</b>\n"
                    f"Твой прогноз для г. {city.capitalize()}:\n\n"
                    f"{advice}"
                )
                await bot.send_message(user_id, text, parse_mode="HTML")
                await asyncio.sleep(0.05)
        except Exception as e:
            print(f"Ошибка рассылки {user_id}: {e}")



@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🌡 Узнать погоду"))
    builder.row(types.KeyboardButton(text="⚙️ Настройки"), types.KeyboardButton(text="ℹ️ Помощь"))

    await message.answer(
        "Привет! Я твой <b>Life Assistant</b>. 🤖\nНажми на кнопку или напиши город.",
        reply_markup=builder.as_markup(resize_keyboard=True),
        parse_mode="HTML"
    )


@dp.message(lambda message: message.text == "🌡 Узнать погоду")
async def ask_city(message: types.Message):
    await message.answer("Введи название города:")


@dp.message()
async def weather_logic(message: types.Message):
    city = message.text.replace('/weather', '').strip()

    if city in ["⚙️ Настройки", "ℹ️ Помощь", ""]:
        await message.answer("Этот раздел в разработке.")
        return

    w_data = await get_weather(city)
    if not w_data:
        await message.answer(f"Город '{city}' не найден. Попробуй еще раз.")
        return


    await set_user_city(message.from_user.id, city)

    advice = await get_ai_recommendation(w_data['temp'], w_data['desc'], w_data['humidity'])

    await message.answer(
        f"📍 <b>{city.capitalize()}</b>\n"
        f"🌡 {w_data['temp']}°C, {w_data['desc']}\n"
        f"💧 Влажность: {w_data['humidity']}%\n\n"
        f"🤖 <b>Совет:</b>\n{advice}",
        parse_mode="HTML"
    )


async def main():
    await init_db()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_forecast, "cron", hour=10, minute=00)
    scheduler.start()

    print("Бот и планировщик запущены!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
