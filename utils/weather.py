import aiohttp
import json
from urllib.parse import quote


async def get_weather(city: str):
    city_cleaned = city.strip()
    safe_city = quote(city_cleaned)
    url = f"https://wttr.in/{safe_city}?format=j1&lang=ru"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return None

                raw_text = await response.text()
                try:
                    data = json.loads(raw_text)
                    if 'current_condition' not in data:
                        return None

                    current = data['current_condition'][0]

                    area_data = data['nearest_area'][0]
                    server_city = area_data['areaName'][0]['value'].lower()
                    region = area_data['region'][0]['value'].lower()
                    country = area_data['country'][0]['value'].lower()

                    user_city_low = city_cleaned.lower()

                    if (user_city_low in server_city or
                            server_city in user_city_low or
                            user_city_low in region or
                            user_city_low in country or
                            "kyiv" in user_city_low or
                            "киев" in user_city_low):

                        return {
                            "temp": current['temp_C'],
                            "desc": current['lang_ru'][0]['value'],
                            "humidity": current['humidity']
                        }
                    else:
                        print(f"DEBUG: Inconsistency. Entered:{city_cleaned}, 
                        Found: {server_city} ({region})")
                        return None

                except Exception as parse_err:
                    print(f"DEBUG:Parsing error: {parse_err}")
                    return None
        except Exception as e:
            print(f"DEBUG: Network Error: {e}")
            return None
