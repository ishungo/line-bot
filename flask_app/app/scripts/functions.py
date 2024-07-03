import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime as dt
from dotenv import load_dotenv
from openai import OpenAI
import pytz
jst = pytz.timezone('Asia/Tokyo')
print(jst)
# Asia/Tokyo

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = SCRIPT_DIR.parent.parent.parent / '.env'
load_dotenv(str(ENV_DIR))
API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")


FIRST_PROMPT = "上記の文章は、以下のどの選択肢に該当する文章ですか？"
FIRST_PROMPT += "\n1. 天気について尋ねる文章"
FIRST_PROMPT += "\n2. その他の質問"
FIRST_PROMPT += "\n回答は「1」もしくは「2」のように数字で答えてください"

WEATHER_PROMPT = "上記の文章はどの都市の天気について尋ねている文章ですか？"
WEATHER_PROMPT += "\n都市名を入力してください. 例: TOKYO"

def generate_text(msg, model):
    client = OpenAI(api_key = API_KEY)
    response = client.chat.completions.create(
        model=model,
        messages = [{"role": "user",
                     "content": msg}],
        max_tokens=500,
        temperature=0.3
    )
    ret = response.choices[0].message.content
    return ret


def create_responce(msg, model):
    first_responce = generate_text(msg + FIRST_PROMPT, model)
    if "1" in first_responce:
        city = generate_text(msg + WEATHER_PROMPT, model)
        ret = get_weather(city)
    elif "2" in first_responce:
        ret = generate_text(msg, model)
    else:
        ret = "解析に失敗しました"
    return ret


def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    params = {
        "q": city,
        "units": "metric",
        "appid": WEATHER_API_KEY,
    }
    # complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

    response = requests.get(base_url, params=params)
    data = response.json()
    # print(data)
    if response.status_code == 200:
        data = response.json()

        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]
        sys = data["sys"]

        temp = main["temp"]
        temp_min = main["temp_min"]
        temp_max = main["temp_max"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]
        wind_speed = wind["speed"]
        wind_deg = wind["deg"]
        sunrise = sys["sunrise"]
        sunset = sys["sunset"]

        ret = f"地名: {data['name']}"
        ret += f"\n国: {sys['country']}"
        ret += f"\n天気: {description.capitalize()}"
        ret += f"\n気温: {temp}°C"
        ret += f"\n最低気温: {temp_min}°"
        ret += f"\n最高気温: {temp_max}°C"
        ret += f"\n気圧: {pressure} hPa"
        ret += f"\n湿度: {humidity}%"
        ret += f"\n風速: {wind_speed} m/s"
        ret += f"\n風向: {wind_deg}°"
        ret += f"\n日の出: {to_jst(dt.fromtimestamp(sunrise))}"
        ret += f"\n日没: {to_jst(dt.fromtimestamp(sunset))}"
    elif response.status_code == 404:
        ret = "天気の取得に失敗しました"
    else:
        ret = "エラーが発生しました"
    return ret


def to_jst(dt):
    return dt.astimezone(jst).strftime('%Y-%m-%d %H:%M:%S')

def main():
    msg = "ubuntuとは何ですか？"
    model = "gpt-3.5-turbo"
    print(generate_text(msg, model))

if __name__ == "__main__":
    # main()
    get_weather("Tokyo")
