import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# botni tokeni 
TOKEN = "5959492476:AAGppTUR8fAdCEp8X8p4V4tpUt7iqkv3Eec"
token_open_weather = "ae369fb3ab507b7a8501b0bf95b9583c"  # saytni tokeni

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# bowlaw
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Assalomu alekum\n"
                        "Siz menga shaxarni yozing \nmen esa sizga Ob-Havo malumotlarini beraman")

# help comandasini bosganda
@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.answer("Men Ob-Havo malumotlarini beruvchi botman")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Yahshi \U00002600',
        'Clouds': 'Bulutli \U00002601',
        'Rain': 'Yomgir \U00002614',
        'Drizzle': 'Yomgir \U00002614',
        'Thunderstorm': 'Momaqaldiroq \U000026A1',
        'Snow': 'Qor \U0001F328',
        'Mist': 'Tuman \U0001F32B',

    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token_open_weather}&units=metric"
        )
        data = r.json()
        city = data["name"]
        weather_main = data["weather"][0]["main"]
        if weather_main in code_to_smile:
            wd = code_to_smile[weather_main]

        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_day = sunset_timestamp - sunrise_timestamp

        await message.answer(f"****  {datetime.datetime.now().strftime('%Y-%m-%d  %H:%M')}   ****\n"
                             f"Shaxardagi xarorat: {city}\nTemperatura: {cur_weather}°C {wd}\n"
                             f"Namlik: {humidity}%\nBosim: {pressure} mm.suv.ust\nShamol tezligi: {wind} m/s\n"
                             f"Quyosh chiqishi: {sunrise_timestamp}\nQuyosh botishi: {sunset_timestamp}\nKun davomiyligi: {length_day}\n"
                             f"*** Kuningiz hayrli otsin!!! ***")

    except:
        await message.reply("\U00002620 Shaxarni notogri kiritingiz \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
