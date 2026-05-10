from groq import AsyncGroq
from config import GROQ_API_KEY

client = AsyncGroq(api_key=GROQ_API_KEY)


async def get_ai_recommendation(temp, desc, humidity):
    user_message = f"Температура: {temp}C, Состояние: {desc}, Влажность: {humidity}%."

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Ты — Life Assistant, профессиональный погодный гид. "
                "На основе данных дай ответ строго в 3 пунктах: "
                "1. Одежда (что надеть сейчас). "
                "2. Аксессуары (нужен ли зонт, очки, шарф). "
                "3. Активность (стоит ли идти гулять или лучше остаться дома). "
                "Пиши кратко, энергично и по делу."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content