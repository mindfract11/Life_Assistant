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
                    f" <b>Good morning!!</b>\n"
                    f"Your forecast for the city. {city.capitalize()}:\n\n"
                    f"{advice}"
                )
                await bot.send_message(user_id, text, parse_mode="HTML")
                await asyncio.sleep(0.05)
        except Exception as e:
            print(f"Mailing error {user_id}: {e}")



@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text=" Check the weather"))
    builder.row(types.KeyboardButton(text=" Setting"), types.KeyboardButton(text=" Help"))

    await message.answer(
        "Hello! I your <b>Life Assistant</b>. \nClick the button or write the city.",
        reply_markup=builder.as_markup(resize_keyboard=True),
        parse_mode="HTML"
    )


@dp.message(lambda message: message.text == "Check the weather ")
async def ask_city(message: types.Message):
    await message.answer("Enter the city name:")


@dp.message()
async def weather_logic(message: types.Message):
    city = message.text.replace('/weather', '').strip()

    if city in ["Setting", " Help", ""]:
        await message.answer("This section is under development.")
        return

    w_data = await get_weather(city)
    if not w_data:
        await message.answer(f"City'{city}' not found. Try again.")
        return


    await set_user_city(message.from_user.id, city)

    advice = await get_ai_recommendation(w_data['temp'], w_data['desc'], w_data['humidity'])

    await message.answer(
        f"<b>{city.capitalize()}</b>\n"
        f"{w_data['temp']}°C, {w_data['desc']}\n"
        f"Humidity: {w_data['humidity']}%\n\n"
        f"<b>Advice:</b>\n{advice}",
        parse_mode="HTML"
    )


async def main():
    await init_db()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_forecast, "cron", hour=10, minute=00)
    scheduler.start()

    print("The bot and scheduler are launched!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
